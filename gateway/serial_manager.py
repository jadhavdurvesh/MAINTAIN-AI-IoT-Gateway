import threading
from collections.abc import Callable

import serial
from serial.tools import list_ports

from gateway.models import SerialDevice
from protocol.parser import parse_line


class SerialManager:
    def __init__(self, baud_rate: int = 115200):
        self.baud_rate = baud_rate
        self._serial = None
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()

    @staticmethod
    def scan() -> list[SerialDevice]:
        return [SerialDevice(p.device, p.description or "Serial device", p.manufacturer or "", p.vid, p.pid) for p in list_ports.comports()]

    def connect(self, port: str, on_payload: Callable[[dict], None], on_error: Callable[[str], None]) -> None:
        self.disconnect()
        self._serial = serial.Serial(port, self.baud_rate, timeout=1)
        self._stop.clear()
        self._thread = threading.Thread(target=self._read_loop, args=(on_payload, on_error), daemon=True)
        self._thread.start()

    def _read_loop(self, on_payload, on_error) -> None:
        while not self._stop.is_set() and self._serial:
            try:
                line = self._serial.readline().decode("utf-8", errors="replace")
                payload = parse_line(line)
                if payload is not None:
                    on_payload(payload)
            except (serial.SerialException, OSError) as exc:
                on_error(str(exc))
                break

    def disconnect(self) -> None:
        self._stop.set()
        if self._serial:
            try:
                self._serial.close()
            except serial.SerialException:
                pass
        self._serial = None

    @property
    def connected(self) -> bool:
        return bool(self._serial and self._serial.is_open)
