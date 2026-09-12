import time
import requests


class ApiClient:
    def __init__(self, url: str, device_key: str, timeout: float = 10):
        self.url = url
        self.device_key = device_key
        self.timeout = timeout

    def send(self, reading_type: str, value: float, unit: str) -> tuple[bool, int | None, str]:
        headers = {"X-Device-Key": self.device_key, "Content-Type": "application/json"}
        payload = {"reading_type": reading_type, "value": value, "unit": unit}
        try:
            response = requests.post(self.url, json=payload, headers=headers, timeout=self.timeout)
            return response.ok, response.status_code, response.text[:200]
        except requests.RequestException as exc:
            return False, None, str(exc)

    def test_connection(self) -> tuple[bool, str]:
        ok, status, message = self.send("gateway_test", 0.0, "status")
        if status == 200:
            return True, "Backend accepted device key"
        if status == 401:
            return False, "Invalid or disabled device key"
        return ok, f"HTTP {status}: {message}" if status else f"Backend unavailable: {message}"

    @staticmethod
    def backoff(attempt: int) -> float:
        return min(30.0, (1.5 ** attempt))
