import json
import threading
import time


class SafetyCommandWorker:
    """Poll durable safety commands and deliver them over the active serial link."""

    def __init__(self, api_url: str, device_key: str, serial_manager, enabled: bool = True):
        self._api_url = api_url
        self._device_key = device_key
        self._serial = serial_manager
        self._enabled = enabled
        self._stop = threading.Event()
        self._lock = threading.Lock()
        self._pending_event_id = None
        self._last_sent_at = 0.0
        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
            name="maintain-safety-command",
        )
        self._thread.start()

    def set_credentials(self, api_url: str, device_key: str) -> None:
        with self._lock:
            self._api_url = api_url
            self._device_key = device_key

    def set_enabled(self, enabled: bool) -> None:
        with self._lock:
            self._enabled = enabled
            if not enabled:
                self._pending_event_id = None
                self._last_sent_at = 0.0

    def acknowledge(self, event_id: int) -> None:
        with self._lock:
            if self._pending_event_id == event_id:
                self._pending_event_id = None
                self._last_sent_at = 0.0
            api_url = self._api_url
            device_key = self._device_key

        if not api_url or not device_key:
            return

        try:
            from gateway.api_client import ApiClient
            ApiClient(api_url, device_key).ack_command(event_id)
        except Exception:
            # The command remains pending in the backend and will be retried
            # by the next poll if acknowledgement delivery fails.
            pass

    def _run(self) -> None:
        from gateway.api_client import ApiClient

        while not self._stop.wait(1.0):
            with self._lock:
                enabled = self._enabled
                api_url = self._api_url
                device_key = self._device_key
                pending_event_id = self._pending_event_id
                last_sent_at = self._last_sent_at

            if not enabled or not api_url or not device_key or not self._serial.connected:
                continue

            try:
                command = ApiClient(api_url, device_key, timeout=5).pending_command()
            except Exception:
                continue

            if not command or not command.get("pending"):
                with self._lock:
                    self._pending_event_id = None
                    self._last_sent_at = 0.0
                continue

            try:
                event_id = int(command["event_id"])
            except (KeyError, TypeError, ValueError):
                continue

            now = time.monotonic()
            if pending_event_id == event_id and now - last_sent_at < 2.0:
                continue

            wire_type = "shutdown_test" if command.get("command_type") == "shutdown_test" else "shutdown"
            wire_command = {
                "type": wire_type,
                "event_id": event_id,
                "reason": command.get("reason", ""),
                "reading_type": command.get("reading_type"),
                "value": command.get("value"),
                "threshold": command.get("threshold"),
            }

            try:
                self._serial.write_line(json.dumps(wire_command, separators=(",", ":")))
            except Exception:
                continue

            with self._lock:
                self._pending_event_id = event_id
                self._last_sent_at = now

    def stop(self) -> None:
        self._stop.set()
        if self._thread.is_alive() and self._thread is not threading.current_thread():
            self._thread.join(timeout=1.5)
