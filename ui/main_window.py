from datetime import datetime
from uuid import uuid4

from PySide6.QtCore import QObject, Signal, QTimer, Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QComboBox, QDialog, QDialogButtonBox, QFormLayout, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox,
    QPushButton, QScrollArea, QVBoxLayout, QWidget
)

from gateway.config import delete_device_key, get_device_key, load_config, save_config, set_device_key
from gateway.device_manager import DeviceManager
from protocol.validator import validate_readings


class DeviceSignals(QObject):
    readings = Signal(str, dict)
    error = Signal(str, str)


class AddDeviceDialog(QDialog):
    def __init__(self, parent=None, device=None, ports=None):
        super().__init__(parent)
        self.setWindowTitle("Pair physical machine")
        self.setMinimumWidth(500)
        form = QFormLayout(self)
        self.name = QLineEdit(device.get("name", "") if device else "")
        self.name.setPlaceholderText("CNC controller / Robot / ESP32 Gateway")
        self.machine = QLineEdit(device.get("machine", "") if device else "")
        self.machine.setPlaceholderText("Machine or asset name")
        self.port = QComboBox(); self.port.setEditable(True)
        for port in ports or []:
            self.port.addItem(port)
        if device and device.get("port") and self.port.findText(device["port"]) < 0:
            self.port.addItem(device["port"])
        if device:
            self.port.setCurrentText(device.get("port", ""))
        self.protocol = QComboBox()
        self.protocol.addItem("Arduino / JSON", "json")
        self.protocol.addItem("Marlin / Ender-3", "marlin")
        self.protocol.setCurrentIndex(max(0, self.protocol.findData(device.get("protocol", "json") if device else "json")))
        self.baud = QComboBox(); self.baud.addItems(["9600", "57600", "115200", "230400"])
        self.baud.setCurrentText(str(device.get("baud_rate", 115200) if device else 115200))
        self.key = QLineEdit(); self.key.setEchoMode(QLineEdit.EchoMode.Password)
        self.key.setPlaceholderText("Machine-specific MAINTAIN AI device key")
        form.addRow("Gateway name", self.name)
        form.addRow("Machine", self.machine)
        form.addRow("Serial port", self.port)
        form.addRow("Protocol", self.protocol)
        form.addRow("Baud rate", self.baud)
        form.addRow("Device key", self.key)
        hint = QLabel("Each physical machine must use its own key generated in MAINTAIN AI.")
        hint.setWordWrap(True); hint.setObjectName("hint")
        form.addRow(hint)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept); buttons.rejected.connect(self.reject); form.addRow(buttons)

    def values(self):
        return {"name": self.name.text().strip(), "machine": self.machine.text().strip(),
                "port": self.port.currentText().strip(), "protocol": self.protocol.currentData(),
                "baud_rate": int(self.baud.currentText()), "device_key": self.key.text().strip()}


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__(); self.setWindowTitle("MAINTAIN AI — Physical IoT Gateway"); self.resize(1220, 800)
        self.config = load_config(); self.api_url = self.config["api_url"]
        self.devices = {}; self.cards = {}
        self.signals = DeviceSignals(); self.signals.readings.connect(self.handle_readings); self.signals.error.connect(self.handle_device_error)
        self.build_ui(); self.restore_devices(); self.refresh_ports()
        self.port_timer = QTimer(self); self.port_timer.timeout.connect(self.refresh_ports); self.port_timer.start(3000)

    def build_ui(self):
        root = QWidget(); outer = QVBoxLayout(root); outer.setContentsMargins(28, 24, 28, 24); outer.setSpacing(16)
        header = QHBoxLayout(); brand = QVBoxLayout()
        title = QLabel("MAINTAIN AI"); title.setObjectName("brand"); title.setFont(QFont("Segoe UI", 25, QFont.Weight.Bold))
        sub = QLabel("Physical machine telemetry gateway"); sub.setObjectName("subtitle"); brand.addWidget(title); brand.addWidget(sub)
        header.addLayout(brand); header.addStretch(); self.gateway_status = QLabel("● Gateway ready"); self.gateway_status.setObjectName("statusPill"); header.addWidget(self.gateway_status); outer.addLayout(header)

        toolbar = QFrame(); toolbar.setObjectName("toolbar"); bar = QHBoxLayout(toolbar); bar.setContentsMargins(14, 12, 14, 12)
        add = QPushButton("＋  Pair Machine"); add.setObjectName("primary"); add.clicked.connect(self.add_device)
        refresh = QPushButton("↻  Scan USB"); refresh.clicked.connect(self.refresh_ports)
        test = QPushButton("Test Backend"); test.clicked.connect(self.test_all_backends)
        self.backend = QLineEdit(self.api_url); self.backend.setPlaceholderText("https://maintain-ai-3.vercel.app or /api/devices/ingest"); self.backend.setMinimumWidth(430)
        bar.addWidget(add); bar.addWidget(refresh); bar.addWidget(test); bar.addStretch(); bar.addWidget(QLabel("Backend")); bar.addWidget(self.backend, 1); outer.addWidget(toolbar)

        summary = QHBoxLayout(); self.device_count = self.make_stat("PAIRED", "0"); self.connected_count = self.make_stat("CONNECTED", "0"); self.upload_count = self.make_stat("READINGS SENT", "0")
        for w in (self.device_count, self.connected_count, self.upload_count): summary.addWidget(w, 1)
        outer.addLayout(summary)

        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.container = QWidget(); self.layout = QVBoxLayout(self.container); self.layout.setContentsMargins(0, 2, 8, 2); self.layout.setSpacing(14); self.layout.addStretch(); self.scroll.setWidget(self.container); outer.addWidget(self.scroll, 1)
        self.empty = QLabel("No physical machines paired yet\nPair an Arduino / ESP32 gateway or a Marlin printer and paste the machine-specific device key."); self.empty.setObjectName("empty"); self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter); self.layout.insertWidget(0, self.empty)
        self.setCentralWidget(root)
        self.setStyleSheet("""
            QMainWindow { background:#08111d; color:#e9f1fa; } QLabel { color:#b7c4d4; }
            #brand { color:#f5f8fc; letter-spacing:1px; } #subtitle,#hint { color:#718197; font-size:12px; }
            #toolbar,#stat,#deviceCard { background:#101b29; border:1px solid #22334a; border-radius:14px; }
            #stat { padding:4px; } #statLabel { color:#6f8097; font-size:10px; font-weight:700; } #statValue { color:#edf3fb; font-size:22px; font-weight:700; }
            #deviceCard { border-radius:16px; } #deviceTitle { color:#f4f7fb; font-size:17px; font-weight:700; } #deviceMeta { color:#718197; font-size:12px; }
            #reading { background:#0b1522; border:1px solid #1d2d42; border-radius:11px; } #readingName { color:#73849b; font-size:11px; } #readingValue { color:#eef4fb; font-size:17px; font-weight:700; }
            #statusPill { background:#122335; border:1px solid #29445e; border-radius:12px; padding:8px 12px; color:#a9bdd0; }
            #empty { color:#65768d; font-size:14px; padding:60px; } QLineEdit,QComboBox { background:#0c1725; color:#eaf1f8; border:1px solid #273951; border-radius:9px; padding:9px; }
            QPushButton { background:#172438; color:#eaf1f8; border:1px solid #2a3d56; border-radius:9px; padding:9px 13px; font-weight:600; } QPushButton:hover { background:#20334c; }
            QPushButton#primary { background:#eaf1f8; color:#08111d; border:none; } QPushButton#primary:hover { background:white; }
        """)

    def make_stat(self, name, value):
        card = QFrame(); card.setObjectName("stat"); box = QVBoxLayout(card); box.setContentsMargins(15,10,15,10); lab = QLabel(name); lab.setObjectName("statLabel"); val = QLabel(value); val.setObjectName("statValue"); box.addWidget(lab); box.addWidget(val); card.value_label = val; return card

    def ports(self): return [d.port for d in DeviceManager(self.api_url).serial.scan()]

    def restore_devices(self):
        for saved in self.config.get("devices", []):
            if saved.get("id"): self.create_device(saved)
        self.update_summary()

    def create_device(self, saved):
        did = saved.get("id") or f"device-{uuid4().hex[:8]}"; record = dict(saved); record["id"] = did
        record.setdefault("name", f"Machine {len(self.devices)+1:02d}"); record.setdefault("machine", "Unpaired machine"); record.setdefault("port", ""); record.setdefault("baud_rate", 115200)
        manager = DeviceManager(self.api_url, int(record["baud_rate"]), did)
        self.devices[did] = {"config":record,"manager":manager,"readings":{},"uploads":0,"last_upload":None}; self.add_card(did); return did

    def add_card(self, did):
        data = self.devices[did]; rec = data["config"]; card = QFrame(); card.setObjectName("deviceCard"); box = QVBoxLayout(card); box.setContentsMargins(18,16,18,16); box.setSpacing(12)
        top = QHBoxLayout(); identity = QVBoxLayout(); title = QLabel(rec["name"]); title.setObjectName("deviceTitle"); meta = QLabel(self.device_meta(rec)); meta.setObjectName("deviceMeta"); identity.addWidget(title); identity.addWidget(meta); top.addLayout(identity); top.addStretch()
        status = QLabel("● Disconnected"); status.setObjectName("deviceMeta"); data["status"] = status; top.addWidget(status)
        for text, slot in (("Edit",self.edit_device),("Connect",self.connect_device),("Disconnect",self.disconnect_device),("Remove",self.remove_device)):
            btn = QPushButton(text); btn.setObjectName("primary" if text=="Connect" else "")
            btn.clicked.connect(lambda _, d=did, f=slot: f(d)); top.addWidget(btn); data[text.lower()] = btn
        data["title"]=title; data["meta"]=meta; box.addLayout(top)
        grid = QGridLayout(); grid.setHorizontalSpacing(10); grid.setVerticalSpacing(10); data["reading_labels"]={}; box.addLayout(grid); data["grid"]=grid
        info = QLabel("Waiting for physical sensor data"); info.setObjectName("deviceMeta"); data["info"]=info; box.addWidget(info)
        self.cards[did]=card; self.layout.insertWidget(self.layout.count()-1, card); self.empty.setVisible(False); self.rebuild_reading_cards(did)

    def rebuild_reading_cards(self, did):
        data=self.devices[did]; grid=data["grid"]
        while grid.count():
            item=grid.takeAt(0); w=item.widget()
            if w: w.deleteLater()
        data["reading_labels"]={}
        names=list(data["readings"].keys()) or ["nozzle_temperature","bed_temperature","x_position","y_position","z_position"]
        for i,name in enumerate(names[:24]):
            box=QFrame(); box.setObjectName("reading"); v=QVBoxLayout(box); v.setContentsMargins(12,9,12,9); n=QLabel(name.replace("_"," ").title()); n.setObjectName("readingName"); val=QLabel("—"); val.setObjectName("readingValue"); v.addWidget(n); v.addWidget(val); data["reading_labels"][name]=val; grid.addWidget(box,i//4,i%4)
        for name,(value,unit) in data["readings"].items():
            if name in data["reading_labels"]: data["reading_labels"][name].setText(f"{value:g} {unit}")

    @staticmethod
    def device_meta(rec): return f"{rec.get('machine') or 'Unpaired machine'}  ·  {rec.get('port') or 'No USB port'}  ·  {rec.get('baud_rate',115200)} baud  ·  {('Marlin' if rec.get('protocol') == 'marlin' else 'JSON')}"

    def add_device(self):
        dialog=AddDeviceDialog(self, ports=self.ports())
        if dialog.exec()!=QDialog.DialogCode.Accepted: return
        v=dialog.values()
        if not v["name"]: v["name"]=f"Machine {len(self.devices)+1:02d}"
        if not v["port"] or not v["device_key"]: QMessageBox.warning(self,"Pair machine","Machine name, serial port and device key are required."); return
        did=self.create_device({k:v[k] for k in ("name","machine","port","baud_rate","protocol")}); self.devices[did]["manager"].set_device_key(v["device_key"]); self.persist(); self.update_summary()

    def edit_device(self,did):
        data=self.devices[did]; dialog=AddDeviceDialog(self,data["config"],self.ports())
        if dialog.exec()!=QDialog.DialogCode.Accepted:return
        v=dialog.values()
        if not v["name"] or not v["port"]: QMessageBox.warning(self,"Machine","Name and serial port are required."); return
        if data["manager"].serial.connected:self.disconnect_device(did)
        data["config"].update({k:v[k] for k in ("name","machine","port","baud_rate","protocol")}); data["manager"].baud_rate=v["baud_rate"]; data["manager"].serial.baud_rate=v["baud_rate"]; data["manager"].set_protocol(v["protocol"])
        if v["device_key"]: data["manager"].set_device_key(v["device_key"])
        data["title"].setText(data["config"]["name"]); data["meta"].setText(self.device_meta(data["config"])); self.persist()

    def remove_device(self,did):
        data=self.devices.get(did)
        if not data:return
        data["manager"].disconnect(); delete_device_key(did); self.cards[did].deleteLater(); self.cards.pop(did,None); self.devices.pop(did,None); self.persist(); self.empty.setVisible(not self.devices); self.update_summary()

    def connect_device(self,did):
        data=self.devices[did]; key=get_device_key(did); rec=data["config"]
        if not key: QMessageBox.warning(self,"Device key","No device key is stored for this machine."); return
        try:
            data["manager"].api_url=self.backend.text().strip() or self.api_url; data["manager"].set_device_key(key); data["manager"].baud_rate=int(rec.get("baud_rate",115200)); data["manager"].serial.baud_rate=data["manager"].baud_rate; data["manager"].set_protocol(rec.get("protocol","json"))
            data["manager"].serial.connect(rec["port"],lambda p,d=did:self.signals.readings.emit(d,p),lambda m,d=did:self.signals.error.emit(d,m))
            data["status"].setText("● Connected · auto-reconnect enabled"); data["connect"].setEnabled(False); data["disconnect"].setEnabled(True); data["info"].setText("USB connected · waiting for telemetry"); self.update_summary()
        except Exception as exc: QMessageBox.critical(self,"Connection failed",str(exc))

    def disconnect_device(self,did):
        data=self.devices.get(did)
        if not data:return
        data["manager"].disconnect(); data["status"].setText("● Disconnected"); data["connect"].setEnabled(True); data["disconnect"].setEnabled(False); data["info"].setText("Disconnected"); self.update_summary()

    def handle_readings(self,did,payload):
        data=self.devices.get(did)
        if not data:return
        readings=validate_readings(payload)
        if not readings: data["info"].setText("Received serial data, but no valid telemetry signals were found"); return
        failures=[]
        for name,value,unit in readings:
            data["readings"][name]=(value,unit)
            ok,status,msg=data["manager"].api().send(name,value,unit)
            if not ok: failures.append(f"{name}: {status or msg}")
        self.rebuild_reading_cards(did)
        if failures: data["status"].setText("● Upload retry queued"); data["info"].setText("Some readings were queued locally · "+"; ".join(failures[:3]))
        else:
            data["status"].setText("● Connected · telemetry flowing"); data["uploads"]+=len(readings); data["last_upload"]=datetime.now(); data["info"].setText(f"Last upload {data['last_upload'].strftime('%H:%M:%S')} · {len(readings)} reading(s)"); self.update_summary()

    def handle_device_error(self,did,message):
        data=self.devices.get(did)
        if not data:return
        # SerialManager reconnects automatically. Do not call disconnect() here.
        data["status"].setText("● USB reconnecting…"); data["info"].setText("Physical device temporarily unavailable; gateway is retrying the same port.")

    def refresh_ports(self):
        count=len(self.ports()); self.gateway_status.setText(f"● Gateway ready · {count} USB serial device(s) detected")

    def test_all_backends(self):
        self.api_url=self.backend.text().strip() or self.api_url; failures=[]; ok_count=0
        for did,data in self.devices.items():
            key=get_device_key(did)
            if not key: failures.append(data["config"]["name"]+": no key"); continue
            good,msg=data["manager"].api().test_connection()
            if good: ok_count+=1
            else: failures.append(data["config"]["name"]+": "+msg)
        QMessageBox.information(self,"Backend test",f"Accepted: {ok_count}\nFailed: {len(failures)}\n"+"\n".join(failures[:8]))

    def persist(self):
        self.config["api_url"]=self.backend.text().strip() or self.api_url; self.config["devices"]=[d["config"] for d in self.devices.values()]; save_config(self.config)

    def update_summary(self):
        self.device_count.value_label.setText(str(len(self.devices))); self.connected_count.value_label.setText(str(sum(1 for d in self.devices.values() if d["manager"].serial.connected))); self.upload_count.value_label.setText(str(sum(d["uploads"] for d in self.devices.values())))

    def closeEvent(self,event):
        self.persist()
        for data in self.devices.values(): data["manager"].disconnect()
        event.accept()


def run():
    app=QApplication.instance() or QApplication([]); window=MainWindow(); window.show(); return app.exec()
