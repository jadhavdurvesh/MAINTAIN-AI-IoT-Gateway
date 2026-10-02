import queue
import threading


class TelemetryWorker:
    """Uploads telemetry off the Qt UI thread."""

    def __init__(self, api_url: str, device_key: str):
        self._api_url = api_url
        self._device_key = device_key
        self._queue = queue.Queue()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True, name="maintain-telemetry-upload")
        self._thread.start()

    def set_credentials(self, api_url: str, device_key: str) -> None:
        self._api_url = api_url
        self._device_key = device_key

    def submit(self, readings, callback=None) -> None:
        if readings:
            self._queue.put((readings, callback))

    def _run(self) -> None:
        from gateway.api_client import ApiClient
        while not self._stop.is_set():
            try:
                readings, callback = self._queue.get(timeout=0.2)
            except queue.Empty:
                continue
            sent = 0
            failures = []
            try:
                client = ApiClient(self._api_url, self._device_key)
                for name, value, unit in readings:
                    ok, status, message = client.send(name, value, unit)
                    if ok:
                        sent += 1
                    else:
                        failures.append(f"{name}: {status or message}")
            except Exception as exc:
                failures.append(str(exc))
            if callback:
                try:
                    callback(sent, failures)
                except Exception:
                    pass
            self._queue.task_done()

    def stop(self) -> None:
        self._stop.set()
        self._thread.join(timeout=1.5)
