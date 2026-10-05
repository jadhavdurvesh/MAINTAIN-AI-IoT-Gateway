import json
import threading
import time


class SafetyCommandWorker:
    """Poll the backend command queue and deliver commands to the connected device."""

    def __init__(self, api_url, device_key, serial_manager):
        self._api_url = api_url
        self._device_key = device_key
        self._serial = serial_manager
        self._stop = threading.Event()
        self._thread = threading.Thread(
            target=self._run,
            daemon=True,
            name="maintain-safety-command",
        )
        self._thread.start()

    def set_credentials(self, api_url, device_key):
        self._api_url = api_url
        self._device_key = device_key

    def _run(self):
        from gateway.api_client import ApiClient

        while not self._stop.wait(1.0):
            if not self._api_url or not self._device_key or not self._serial.connected:
                continue

            try:
                command = ApiClient(
                    self._api_url,
                    self._device_key,
                    timeout=5,
                ).pending_command()
            except Exception:
                continue

            if not command or not command.get("pending"):
                continue

            try:
                event_id = int(command["event_id"])
            except (KeyError, TypeError, ValueError):
                continue

            command_type = (
                "shutdown_test"
                if command.get("command_type") == "shutdown_test"
                else "shutdown"
            )

            payload = {
                "type": command_type,
                "event_id": event_id,
                "reason": command.get("reason", ""),
                "reading_type": command.get("reading_type"),
                "value": command.get("value"),
                "threshold": command.get("threshold"),
            }

            try:
                self._serial.write_line(
                    json.dumps(payload, separators=(",", ":"))
                )
            except Exception:
                continue

    def acknowledge(self, event_id):
        if not self._api_url or not self._device_key:
            return

        try:
            from gateway.api_client import ApiClient

            ApiClient(
                self._api_url,
                self._device_key,
                timeout=5,
            ).ack_command(event_id)
        except Exception:
            # The command remains pending and will be retried.
            pass

    def stop(self):
        self._stop.set()
        if (
            self._thread.is_alive()
            and self._thread is not threading.current_thread()
        ):
            self._thread.join(timeout=1.5)
