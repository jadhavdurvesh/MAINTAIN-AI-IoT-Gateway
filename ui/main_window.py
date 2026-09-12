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
    def __init__(self, parent=None, device=None):
        super().__init__(parent)
        self.setWindowTitle("Add device")
        self.setMinimumWidth(440)
        form = QFormLayout(self)
        self.name = QLineEdit(device.get("name", "") if device else "")
        self.name.setPlaceholderText("e.g. Machine A Controller")
        self.machine = QLineEdit(device.get("machine", "") if device else "")
        self.machine.setPlaceholderText("Machine name or asset")
        self.port = QComboBox()
        self.port.setEditable(True)
        self.baud = QComboBox()
        self.baud.addItems(["9600", "57600", "115200", "230400"])
        self.baud.setCurrentText(str(device.get("baud_rate", 115200) if device else 115200))
        self.key = QLineEdit()
        self.key.setEchoMode(QLineEdit.EchoMode.Password)
        self.key.setPlaceholderText("Machine IoT device key")
        if device:
            self.port.addItem(device.get("port", ""))
        form.addRow("Device name", self.name)
        form.addRow("Machine", self.machine)
        form.addRow("Serial port", self.port)
        form.addRow("Baud rate", self.baud)
        form.addRow("Device key", self.key)
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Cancel | QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        form.addRow(buttons)

    def values(self):
        return {
            "name": self.name.text().strip(),
            "machine": self.machine.text().strip(),
            "port": self.port.currentText().strip(),
            "baud_rate": int(self.baud.currentText()),
            "device_key": self.key.text().strip(),
        }


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAINTAIN AI — IoT Gateway")
        self.resize(1180, 760)
        self.config = load_config()
        self.api_url = self.config["api_url"]
        self.devices = {}
        self.cards = {}
        self.signals = DeviceSignals()
        self.signals.readings.connect(self.handle_readings)
        self.signals.error.connect(self.handle_device_error)
        self.build_ui()
        self.restore_devices()
        self.refresh_ports()
        self.port_timer = QTimer(self)
        self.port_timer.timeout.connect(self.refresh_ports)
        self.port_timer.start(3000)

    def build_ui(self):
        root = QWidget()
        outer = QVBoxLayout(root)
        outer.setContentsMargins(30, 26, 30, 26)
        outer.setSpacing(18)

        header = QHBoxLayout()
        brand = QVBoxLayout()
        title = QLabel("MAINTAIN AI")
        title.setObjectName("brand")
        title.setFont(QFont("Segoe UI", 26, QFont.Weight.Bold))
        subtitle = QLabel("Industrial IoT Gateway")
        subtitle.setObjectName("subtitle")
        brand.addWidget(title)
        brand.addWidget(subtitle)
        header.addLayout(brand)
        header.addStretch()
        self.gateway_status = QLabel("● Gateway ready")
        self.gateway_status.setObjectName("statusPill")
        header.addWidget(self.gateway_status, alignment=Qt.AlignmentFlag.AlignTop)
        outer.addLayout(header)

        toolbar = QFrame()
        toolbar.setObjectName("toolbar")
        bar = QHBoxLayout(toolbar)
        bar.setContentsMargins(16, 12, 16, 12)
        add = QPushButton("＋  Add Device")
        add.setObjectName("primary")
        add.clicked.connect(self.add_device)
        refresh = QPushButton("↻  Refresh")
        refresh.clicked.connect(self.refresh_ports)
        self.backend = QLineEdit(self.api_url)
        self.backend.setPlaceholderText("MAINTAIN AI ingestion endpoint")
        self.backend.setMinimumWidth(360)
        bar.addWidget(add)
        bar.addWidget(refresh)
        bar.addStretch()
        bar.addWidget(QLabel("Backend"))
        bar.addWidget(self.backend, 1)
        outer.addWidget(toolbar)

        summary = QHBoxLayout()
        self.device_count = self.make_stat("DEVICES", "0")
        self.connected_count = self.make_stat("CONNECTED", "0")
        self.upload_count = self.make_stat("UPLOADS", "0")
        self.summary_widgets = (self.device_count, self.connected_count, self.upload_count)
        for widget in self.summary_widgets:
            summary.addWidget(widget, 1)
        outer.addLayout(summary)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)
        self.device_container = QWidget()
        self.device_layout = QVBoxLayout(self.device_container)
        self.device_layout.setContentsMargins(0, 2, 8, 2)
        self.device_layout.setSpacing(14)
        self.device_layout.addStretch()
        self.scroll.setWidget(self.device_container)
        outer.addWidget(self.scroll, 1)

        self.empty = QLabel("No devices connected yet\nAdd a serial device to begin collecting machine data.")
        self.empty.setObjectName("empty")
        self.empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.device_layout.insertWidget(0, self.empty)

        self.setCentralWidget(root)
        self.setStyleSheet("""
            QMainWindow { background: #0a101a; color: #e8eef7; }
            QLabel { color: #b9c5d6; }
            #brand { color: #f4f7fb; letter-spacing: 1px; }
            #subtitle { color: #718198; font-size: 13px; }
            #toolbar, #stat, #deviceCard { background: #111a28; border: 1px solid #223047; border-radius: 14px; }
            #toolbar { border-radius: 12px; }
            #stat { padding: 4px; }
            #statLabel { color: #6f7f95; font-size: 11px; font-weight: 600; }
            #statValue { color: #eef4fc; font-size: 22px; font-weight: 700; }
            #deviceCard { border-radius: 16px; }
            #deviceTitle { color: #f2f6fb; font-size: 16px; font-weight: 650; }
            #deviceMeta { color: #718198; font-size: 12px; }
            #reading { background: #0c1522; border: 1px solid #1c2a3e; border-radius: 11px; }
            #readingName { color: #718198; font-size: 11px; }
            #readingValue { color: #edf3fa; font-size: 18px; font-weight: 650; }
            #statusPill { background: #132333; border: 1px solid #29415b; border-radius: 12px; padding: 8px 12px; color: #9bb4ca; }
            #empty { color: #617188; font-size: 14px; padding: 55px; }
            QLineEdit, QComboBox { background: #0d1725; color: #eaf1f8; border: 1px solid #26364d; border-radius: 9px; padding: 9px 10px; }
            QPushButton { background: #172336; color: #eaf1f8; border: 1px solid #2b3c54; border-radius: 9px; padding: 9px 14px; font-weight: 600; }
            QPushButton:hover { background: #20324a; }
            QPushButton#primary { background: #eaf1f8; color: #0a101a; border: none; }
            QPushButton#primary:hover { background: #ffffff; }
        """)

    def make_stat(self, name, value):
        card = QFrame(); card.setObjectName("stat")
        layout = QVBoxLayout(card); layout.setContentsMargins(15, 10, 15, 10)
        label = QLabel(name); label.setObjectName("statLabel")
        val = QLabel(value); val.setObjectName("statValue")
        layout.addWidget(label); layout.addWidget(val)
        card.value_label = val
        return card

    def restore_devices(self):
        for saved in self.config.get("devices", []):
            if saved.get("id"):
                self.create_device(saved)
        self.update_summary()

    def create_device(self, saved):
        device_id = saved.get("id") or f"device-{uuid4().hex[:8]}"
        record = dict(saved)
        record["id"] = device_id
        record.setdefault("name", f"Device {len(self.devices) + 1:02d}")
        record.setdefault("machine", "")
        record.setdefault("port", "")
        record.setdefault("baud_rate", 115200)
        manager = DeviceManager(self.api_url, int(record["baud_rate"]), device_id)
        self.devices[device_id] = {"config": record, "manager": manager, "readings": {}, "uploads": 0, "last_upload": None}
        self.add_card(device_id)
        return device_id

    def add_card(self, device_id):
        data = self.devices[device_id]
        record = data["config"]
        card = QFrame(); card.setObjectName("deviceCard")
        layout = QVBoxLayout(card); layout.setContentsMargins(18, 16, 18, 16); layout.setSpacing(12)
        top = QHBoxLayout()
        identity = QVBoxLayout()
        title = QLabel(record["name"]); title.setObjectName("deviceTitle")
        meta = QLabel(self.device_meta(record)); meta.setObjectName("deviceMeta")
        identity.addWidget(title); identity.addWidget(meta)
        top.addLayout(identity); top.addStretch()
        status = QLabel("● Disconnected"); status.setObjectName("deviceMeta")
        data["status"] = status; top.addWidget(status)
        edit = QPushButton("Edit"); edit.clicked.connect(lambda _, did=device_id: self.edit_device(did))
        connect = QPushButton("Connect"); connect.setObjectName("primary")
        connect.clicked.connect(lambda _, did=device_id: self.connect_device(did))
        disconnect = QPushButton("Disconnect"); disconnect.setEnabled(False)
        disconnect.clicked.connect(lambda _, did=device_id: self.disconnect_device(did))
        remove = QPushButton("Remove")
        remove.clicked.connect(lambda _, did=device_id: self.remove_device(did))
        data["title"] = title; data["meta"] = meta; data["connect"] = connect; data["disconnect"] = disconnect
        top.addWidget(edit); top.addWidget(connect); top.addWidget(disconnect); top.addWidget(remove)
        layout.addLayout(top)

        grid = QGridLayout(); grid.setHorizontalSpacing(10); grid.setVerticalSpacing(10)
        data["reading_labels"] = {}
        for index, (name, label) in enumerate((("temperature", "Temperature"), ("humidity", "Humidity"), ("vibration", "Vibration"), ("current", "Current"))):
            box = QFrame(); box.setObjectName("reading")
            box_layout = QVBoxLayout(box); box_layout.setContentsMargins(13, 10, 13, 10)
            n = QLabel(label); n.setObjectName("readingName")
            value = QLabel("—"); value.setObjectName("readingValue")
            box_layout.addWidget(n); box_layout.addWidget(value)
            data["reading_labels"][name] = value
            grid.addWidget(box, index // 4, index % 4)
        layout.addLayout(grid)
        footer = QHBoxLayout()
        info = QLabel("Waiting for data")
        info.setObjectName("deviceMeta")
        data["info"] = info
        footer.addWidget(info); footer.addStretch()
        layout.addLayout(footer)
        self.cards[device_id] = card
        self.device_layout.insertWidget(self.device_layout.count() - 1, card)
        self.empty.setVisible(False)

    @staticmethod
    def device_meta(record):
        machine = record.get("machine") or "Unpaired machine"
        port = record.get("port") or "No serial port"
        return f"{machine}  ·  {port}  ·  {record.get('baud_rate', 115200)} baud"

    def add_device(self):
        dialog = AddDeviceDialog(self)
        for device in self.devices.values():
            port = device["config"].get("port")
            if port: dialog.port.addItem(port)
        for item in self.manager_ports():
            if dialog.port.findText(item) < 0: dialog.port.addItem(item)
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        values = dialog.values()
        if not values["name"]: values["name"] = f"Device {len(self.devices) + 1:02d}"
        if not values["port"]:
            QMessageBox.warning(self, "Device", "Select a serial port.")
            return
        if not values["device_key"]:
            QMessageBox.warning(self, "Device key", "Enter the machine IoT device key.")
            return
        device_id = self.create_device({k: values[k] for k in ("name", "machine", "port", "baud_rate")})
        set_device_key(device_id, values["device_key"])
        self.devices[device_id]["manager"].set_device_key(values["device_key"])
        self.persist()
        self.update_summary()

    def edit_device(self, device_id):
        data = self.devices[device_id]; dialog = AddDeviceDialog(self, data["config"])
        for item in self.manager_ports():
            if dialog.port.findText(item) < 0: dialog.port.addItem(item)
        dialog.key.setText("")
        if dialog.exec() != QDialog.DialogCode.Accepted:
            return
        values = dialog.values()
        if not values["name"] or not values["port"]:
            QMessageBox.warning(self, "Device", "Device name and serial port are required.")
            return
        if data["manager"].serial.connected:
            self.disconnect_device(device_id)
        record = data["config"]
        record.update({k: values[k] for k in ("name", "machine", "port", "baud_rate")})
        data["manager"].baud_rate = values["baud_rate"]
        if values["device_key"]:
            data["manager"].set_device_key(values["device_key"])
        data["title"].setText(record["name"]); data["meta"].setText(self.device_meta(record))
        self.persist(); self.update_summary()

    def remove_device(self, device_id):
        data = self.devices.get(device_id)
        if not data: return
        if data["manager"].serial.connected:
            data["manager"].disconnect()
        delete_device_key(device_id)
        card = self.cards.pop(device_id, None)
        if card: card.deleteLater()
        self.devices.pop(device_id, None)
        self.persist(); self.update_summary()
        self.empty.setVisible(not self.devices)

    def connect_device(self, device_id):
        data = self.devices[device_id]; record = data["config"]; manager = data["manager"]
        key = get_device_key(device_id)
        if not key:
            QMessageBox.warning(self, "Device key", f"No device key is stored for {record['name']}.")
            return
        port = record.get("port", "")
        if not port:
            QMessageBox.warning(self, "Serial", "Select a serial port first.")
            return
        try:
            manager.api_url = self.backend.text().strip() or self.api_url
            manager.baud_rate = int(record.get("baud_rate", 115200))
            manager.set_device_key(key)
            manager.serial.connect(port, lambda payload, did=device_id: self.signals.readings.emit(did, payload), lambda message, did=device_id: self.signals.error.emit(did, message))
            data["status"].setText("● Connected")
            data["connect"].setEnabled(False); data["disconnect"].setEnabled(True)
            data["info"].setText("Connected · waiting for sensor data")
            self.persist(); self.update_summary()
        except Exception as exc:
            QMessageBox.critical(self, "Connection failed", str(exc))

    def disconnect_device(self, device_id):
        data = self.devices.get(device_id)
        if not data: return
        data["manager"].disconnect()
        data["status"].setText("● Disconnected")
        data["connect"].setEnabled(True); data["disconnect"].setEnabled(False)
        data["info"].setText("Disconnected")
        self.update_summary()

    def handle_readings(self, device_id, payload):
        data = self.devices.get(device_id)
        if not data: return
        readings = validate_readings(payload)
        if not readings:
            data["info"].setText("Received data, but no supported valid readings were found")
            return
        failures = []
        for name, value, unit in readings:
            data["readings"][name] = (value, unit)
            if name in data["reading_labels"]:
                data["reading_labels"][name].setText(f"{value:g} {unit}")
            ok, status, message = data["manager"].api().send(name, value, unit)
            if not ok: failures.append(f"{name}: {status or message}")
        if failures:
            data["status"].setText("● Backend unavailable")
            data["info"].setText("Upload failed · " + "; ".join(failures))
        else:
            data["status"].setText("● Connected")
            data["uploads"] += len(readings)
            data["last_upload"] = datetime.now()
            data["info"].setText(f"Last upload {data['last_upload'].strftime('%H:%M:%S')} · {len(readings)} reading(s)")
            self.update_summary()

    def handle_device_error(self, device_id, message):
        data = self.devices.get(device_id)
        if not data: return
        data["manager"].disconnect()
        data["status"].setText("● Serial error")
        data["connect"].setEnabled(True); data["disconnect"].setEnabled(False)
        data["info"].setText("Serial error: " + message)
        self.update_summary()

    def manager_ports(self):
        return [device.port for device in DeviceManager.scan_ports()] if hasattr(DeviceManager, "scan_ports") else [d.port for d in self.devices_for_scan()]

    def devices_for_scan(self):
        return DeviceManager(self.api_url).serial.scan()

    def refresh_ports(self):
        ports = self.devices_for_scan()
        known = {d["config"].get("port") for d in self.devices.values()}
        for device in ports:
            if device.port in known:
                continue
        # Keep the currently selected device ports visible; the dialog rescans on open.
        self.gateway_status.setText(f"● Gateway ready · {len(ports)} serial device(s) detected")

    def persist(self):
        self.config["api_url"] = self.backend.text().strip() or self.api_url
        self.config["devices"] = [d["config"] for d in self.devices.values()]
        save_config(self.config)

    def update_summary(self):
        total = len(self.devices)
        connected = sum(1 for d in self.devices.values() if d["manager"].serial.connected)
        uploads = sum(d["uploads"] for d in self.devices.values())
        self.device_count.value_label.setText(str(total))
        self.connected_count.value_label.setText(str(connected))
        self.upload_count.value_label.setText(str(uploads))

    def closeEvent(self, event):
        self.persist()
        for data in self.devices.values():
            data["manager"].disconnect()
        event.accept()


def run():
    app = QApplication.instance() or QApplication([])
    window = MainWindow(); window.show(); return app.exec()
