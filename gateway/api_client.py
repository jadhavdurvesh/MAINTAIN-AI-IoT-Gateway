import json
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path

import requests

QUEUE_DIR = Path.home() / ".maintain-ai-iot-gateway"
QUEUE_FILE = QUEUE_DIR / "telemetry_queue.sqlite3"


class ApiClient:
    def __init__(self, url: str, device_key: str, timeout: float = 10):
        self.url = url
        self.device_key = device_key
        self.timeout = timeout
        QUEUE_DIR.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(QUEUE_FILE) as db:
            db.execute(
                "CREATE TABLE IF NOT EXISTS telemetry_queue ("
                "id INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT UNIQUE NOT NULL,"
                "payload TEXT NOT NULL, created_at TEXT NOT NULL)"
            )

    def _headers(self) -> dict[str, str]:
        return {"X-Device-Key": self.device_key, "Content-Type": "application/json"}

    def _post(self, payload: dict) -> requests.Response:
        return requests.post(self.url, json=payload, headers=self._headers(), timeout=self.timeout)

    def _queue(self, event_id: str, payload: dict) -> None:
        with sqlite3.connect(QUEUE_FILE) as db:
            db.execute(
                "INSERT OR IGNORE INTO telemetry_queue(event_id, payload, created_at) VALUES (?, ?, ?)",
                (event_id, json.dumps(payload), datetime.now(timezone.utc).isoformat()),
            )

    def _flush_queue(self) -> None:
        with sqlite3.connect(QUEUE_FILE) as db:
            rows = db.execute(
                "SELECT id, event_id, payload FROM telemetry_queue ORDER BY id LIMIT 100"
            ).fetchall()

        for row_id, event_id, raw_payload in rows:
            try:
                response = self._post(json.loads(raw_payload))
            except requests.RequestException:
                return
            if response.ok or response.status_code == 409:
                with sqlite3.connect(QUEUE_FILE) as db:
                    db.execute("DELETE FROM telemetry_queue WHERE id = ?", (row_id,))
                continue
            if 500 <= response.status_code:
                return
            # Permanent client-side validation/auth failures should not block
            # the rest of the queue forever.
            if 400 <= response.status_code < 500:
                with sqlite3.connect(QUEUE_FILE) as db:
                    db.execute("DELETE FROM telemetry_queue WHERE id = ?", (row_id,))
                continue
            return

    def send(
        self,
        reading_type: str,
        value: float,
        unit: str,
        event_id: str | None = None,
        recorded_at: str | None = None,
    ) -> tuple[bool, int | None, str]:
        event_id = event_id or str(uuid.uuid4())
        payload = {
            "reading_type": reading_type,
            "value": value,
            "unit": unit,
            "event_id": event_id,
            "recorded_at": recorded_at or datetime.now(timezone.utc).isoformat(),
        }

        try:
            self._flush_queue()
            response = self._post(payload)
            if response.ok or response.status_code == 409:
                return True, response.status_code, response.text[:200]
            if 500 <= response.status_code or response.status_code == 408:
                self._queue(event_id, payload)
            return False, response.status_code, response.text[:200]
        except requests.RequestException as exc:
            self._queue(event_id, payload)
            return False, None, str(exc)

    def test_connection(self) -> tuple[bool, str]:
        try:
            response = requests.post(
                self.url.removesuffix("/api/devices/ingest").rstrip("/") + "/api/devices/ping",
                headers=self._headers(),
                timeout=self.timeout,
            )
            if response.ok:
                data = response.json()
                return True, f"Backend accepted device key for {data.get('machine', 'machine')}"
            if response.status_code == 401:
                return False, "Invalid or disabled device key"
            return False, f"HTTP {response.status_code}: {response.text[:200]}"
        except requests.RequestException as exc:
            return False, f"Backend unavailable: {exc}"
