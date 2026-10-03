import threading
import time
from collections.abc import Callable

import serial
from serial.tools import list_ports

from gateway.models import SerialDevice
from protocol.parser import parse_line


class SerialManager:
    """Serial reader with bounded automatic reconnect for physical gateways."""

    def __init__(
        self,
        baud_rate: int = 115200,
        reconnect: bool = True,
        protocol: str = "json",
        poll_interval: float = 2.0,
    ):
        self.baud_rate = baud_rate
        self.reconnect_enabled = reconnect
        self.protocol = protocol
        self.poll_interval = poll_interval
        self._serial = None
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._port = ""
        self._on_payload = None
        self._on_error = None
        self._lock = threading.Lock()

    @staticmethod
    def scan() -> list[SerialDevice]:
        return [
            SerialDevice(
                p.device,
                p.description or "Serial device",
                p.manufacturer or "",
                p.vid,
                p.pid,
            )
            for p in list_ports.comports()
        ]

    def connect(
        self,
        port: str,
        on_payload: Callable[[dict], None],
        on_error: Callable[[str], None],
    ) -> None:
        self.disconnect()
        self._port = port
        self._on_payload = on_payload
        self._on_error = on_error
        self._stop.clear()
        self._thread = threading.Thread(
            target=self._read_loop,
            daemon=True,
            name=f"maintain-serial-{port}",
        )
        self._thread.start()

    def _open(self):
        with self._lock:
            if self._serial and self._serial.is_open:
                return
            self._serial = serial.Serial(self._port, self.baud_rate, timeout=1)
            if self.protocol == "marlin":
                self._serial.write(b"M105\nM114\n")
                self._serial.flush()

    def _poll_marlin(self) -> None:
        if self.protocol != "marlin":
            return
        with self._lock:
            if self._serial and self._serial.is_open:
                # Poll both thermal data and the current XYZ tool position.
                # M105 reports temperatures; M114 reports X/Y/Z/E position.
                self._serial.write(b"M105\nM114\n")
                self._serial.flush()

    def _read_loop(self) -> None:
        first_failure_reported = False
        next_poll = 0.0

        while not self._stop.is_set():
            try:
                self._open()
                first_failure_reported = False
                next_poll = time.monotonic()

                while not self._stop.is_set() and self._serial and self._serial.is_open:
                    if self.protocol == "marlin" and time.monotonic() >= next_poll:
                        self._poll_marlin()
                        next_poll = time.monotonic() + self.poll_interval

                    line = self._serial.readline().decode("utf-8", errors="replace")
                    payload = parse_line(line)
                    if payload is not None and self._on_payload:
                        self._on_payload(payload)

            except (serial.SerialException, OSError) as exc:
                with self._lock:
                    try:
                        if self._serial:
                            self._serial.close()
                    except Exception:
                        pass
                    self._serial = None
                if not self.reconnect_enabled:
                    if self._on_error:
                        self._on_error(str(exc))
                    break
                if not first_failure_reported and self._on_error:
                    self._on_error(f"temporary serial link loss: {exc}")
                    first_failure_reported = True
                for _ in range(20):
                    if self._stop.is_set():
                        return
                    time.sleep(0.1)
            except Exception as exc:
                if self._on_error:
                    self._on_error(str(exc))
                if not self.reconnect_enabled:
                    break
                time.sleep(2)

    def disconnect(self) -> None:
        self._stop.set()
        with self._lock:
            if self._serial:
                try:
                    self._serial.close()
                except serial.SerialException:
                    pass
            self._serial = None
        thread = self._thread
        if thread and thread.is_alive() and thread is not threading.current_thread():
            thread.join(timeout=1.5)
        self._thread = None

    @property
    def connected(self) -> bool:
        with self._lock:
            return bool(self._serial and self._serial.is_open)
