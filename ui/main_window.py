from datetime import datetime

from PySide6.QtCore import QObject, Signal, QTimer
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication, QComboBox, QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout, QWidget
)

from gateway.config import load_config, save_config
from gateway.device_manager import DeviceManager
from protocol.validator import validate_readings


class BridgeSignals(QObject):
    readings = Signal(dict)
    error = Signal(str)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MAINTAIN AI — IoT Gateway")
        self.resize(980, 680)
        self.config = load_config()
        self.manager = DeviceManager(self.config["api_url"], int(self.config["baud_rate"]))
        self.signals = BridgeSignals()
        self.signals.readings.connect(self.handle_readings)
        self.signals.error.connect(self.handle_serial_error)
        self.last_upload = None
        self.build_ui()
        self.refresh_ports()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_ports)
        self.timer.start(3000)

    def build_ui(self):
        root = QWidget(); outer = QVBoxLayout(root); outer.setContentsMargins(28, 24, 28, 24); outer.setSpacing(18)
        title = QLabel("MAINTAIN AI"); title.setFont(QFont("Segoe UI", 25, QFont.Weight.Bold))
        subtitle = QLabel("IoT Gateway  •  Wired machine connectivity")
        outer.addWidget(title); outer.addWidget(subtitle)

        connection = QFrame(); connection.setObjectName("card"); form = QFormLayout(connection); form.setContentsMargins(22, 18, 22, 18)
        self.port = QComboBox(); self.port.setMinimumWidth(260)
        self.baud = QComboBox(); self.baud.addItems(["9600", "57600", "115200", "230400"]); self.baud.setCurrentText(str(self.config["baud_rate"]))
        self.key = QLineEdit(self.manager.device_key); self.key.setEchoMode(QLineEdit.EchoMode.Password); self.key.setPlaceholderText("Machine IoT device key")
        self.machine = QLineEdit(); self.machine.setPlaceholderText("Optional machine name / label")
        self.api = QLineEdit(self.config["api_url"])
        form.addRow("Serial Port", self.port); form.addRow("Baud Rate", self.baud); form.addRow("Machine", self.machine); form.addRow("Device Key", self.key); form.addRow("Ingestion API", self.api)
        outer.addWidget(connection)

        actions = QHBoxLayout(); self.refresh = QPushButton("Refresh Ports"); self.connect_btn = QPushButton("Connect Arduino"); self.test_btn = QPushButton("Test Backend"); self.disconnect_btn = QPushButton("Disconnect")
        for b in (self.refresh, self.connect_btn, self.test_btn, self.disconnect_btn): actions.addWidget(b)
        self.refresh.clicked.connect(self.refresh_ports); self.connect_btn.clicked.connect(self.connect_serial); self.test_btn.clicked.connect(self.test_backend); self.disconnect_btn.clicked.connect(self.disconnect)
        outer.addLayout(actions)

        status_card = QFrame(); status_card.setObjectName("card"); status_grid = QGridLayout(status_card); status_grid.setContentsMargins(22, 18, 22, 18)
        self.serial_status = QLabel("● Disconnected"); self.backend_status = QLabel("● Not tested"); self.machine_status = QLabel("Not paired"); self.last_status = QLabel("No readings yet")
        status_grid.addWidget(QLabel("Arduino"), 0, 0); status_grid.addWidget(self.serial_status, 0, 1); status_grid.addWidget(QLabel("Backend"), 1, 0); status_grid.addWidget(self.backend_status, 1, 1); status_grid.addWidget(QLabel("Machine"), 2, 0); status_grid.addWidget(self.machine_status, 2, 1); status_grid.addWidget(QLabel("Last upload"), 3, 0); status_grid.addWidget(self.last_status, 3, 1)
        outer.addWidget(status_card)

        sensor_card = QFrame(); sensor_card.setObjectName("card"); grid = QGridLayout(sensor_card); grid.setContentsMargins(22, 20, 22, 20)
        self.sensor_labels = {}
        for index, (name, label) in enumerate([("temperature", "Temperature"), ("humidity", "Humidity"), ("vibration", "Vibration"), ("current", "Current")]):
            box = QFrame(); box.setObjectName("sensor"); layout = QVBoxLayout(box); layout.addWidget(QLabel(label)); value = QLabel("—"); value.setFont(QFont("Segoe UI", 22, QFont.Weight.Bold)); layout.addWidget(value); self.sensor_labels[name] = value; grid.addWidget(box, index // 2, index % 2)
        outer.addWidget(sensor_card); outer.addStretch()
        self.log = QLabel("Ready. Connect an Arduino sending one JSON object per line."); outer.addWidget(self.log)
        self.setCentralWidget(root)
        self.setStyleSheet("""
            QMainWindow { background: #0b1220; color: #e8eef8; }
            QLabel { color: #c7d2e2; }
            QLineEdit, QComboBox { background: #111d2e; color: #eef5ff; border: 1px solid #26364d; border-radius: 9px; padding: 9px; }
            QPushButton { background: #17263a; color: #eef5ff; border: 1px solid #30445e; border-radius: 9px; padding: 10px 15px; }
            QPushButton:hover { background: #20344f; }
            #card { background: #101b2b; border: 1px solid #22334b; border-radius: 14px; }
            #sensor { background: #0d1726; border: 1px solid #21334b; border-radius: 12px; padding: 8px; }
        """)

    def refresh_ports(self):
        current = self.port.currentData() or self.port.currentText()
        devices = self.manager.serial.scan(); self.port.clear()
        for d in devices: self.port.addItem(f"{d.port} — {d.description}", d.port)
        if current:
            i = self.port.findData(current)
            if i >= 0: self.port.setCurrentIndex(i)

    def connect_serial(self):
        if not self.port.currentData(): return QMessageBox.warning(self, "Serial", "No serial port selected.")
        self.manager.baud_rate = int(self.baud.currentText())
        self.manager.set_device_key(self.key.text()); self.manager.api_url = self.api.text().strip()
        try:
            self.manager.serial.connect(self.port.currentData(), self.signals.readings.emit, self.signals.error.emit)
            self.serial_status.setText("● Connected"); self.log.setText("Arduino connected. Waiting for sensor data…")
            self.save()
        except Exception as exc: QMessageBox.critical(self, "Connection failed", str(exc))

    def disconnect(self):
        self.manager.serial.disconnect(); self.serial_status.setText("● Disconnected"); self.log.setText("Arduino disconnected.")

    def test_backend(self):
        self.manager.set_device_key(self.key.text()); self.manager.api_url = self.api.text().strip(); ok, message = self.manager.test_backend(); self.backend_status.setText("● Connected" if ok else "● Unavailable"); self.log.setText(message); self.save()

    def handle_readings(self, payload):
        readings = validate_readings(payload)
        if not readings: self.log.setText("Received JSON, but no supported valid readings were found."); return
        self.backend_status.setText("● Uploading")
        failures = []
        for name, value, unit in readings:
            self.sensor_labels.get(name, QLabel()).setText(f"{value:g} {unit}") if name in self.sensor_labels else None
            ok, status, message = self.manager.api().send(name, value, unit)
            if not ok: failures.append(f"{name}: {status or message}")
        if failures: self.backend_status.setText("● Unavailable"); self.log.setText("Upload failed — " + "; ".join(failures))
        else:
            self.backend_status.setText("● Connected"); self.last_upload = datetime.now(); self.last_status.setText(self.last_upload.strftime("%H:%M:%S")); self.log.setText(f"Uploaded {len(readings)} sensor reading(s) successfully.")

    def handle_serial_error(self, message):
        self.serial_status.setText("● Serial disconnected"); self.log.setText("Serial error: " + message)

    def save(self):
        save_config({"api_url": self.api.text().strip(), "baud_rate": int(self.baud.currentText()), "port": self.port.currentData() or ""})

    def closeEvent(self, event):
        self.save(); self.manager.serial.disconnect(); event.accept()


def run():
    app = QApplication.instance() or QApplication([])
    window = MainWindow(); window.show(); return app.exec()
