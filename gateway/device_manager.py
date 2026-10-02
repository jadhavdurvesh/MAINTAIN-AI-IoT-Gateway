from gateway.api_client import ApiClient
from gateway.config import get_device_key, set_device_key
from gateway.serial_manager import SerialManager
from gateway.telemetry_worker import TelemetryWorker


class DeviceManager:
    """One independent serial/backend connection for one paired machine."""

    def __init__(
        self,
        api_url: str,
        baud_rate: int = 115200,
        device_id: str = "default",
        protocol: str = "json",
    ):
        self.device_id = device_id
        self.serial = SerialManager(baud_rate, protocol=protocol)
        self.api_url = api_url
        self.protocol = protocol
        self.device_key = get_device_key(device_id)
        self.uploader = TelemetryWorker(api_url, self.device_key)

    def set_protocol(self, protocol: str) -> None:
        self.protocol = protocol
        self.serial.protocol = protocol

    def set_device_key(self, value: str) -> None:
        self.device_key = value.strip()
        set_device_key(self.device_id, self.device_key)
        self.uploader.set_credentials(self.api_url, self.device_key)

    def set_api_url(self, value: str) -> None:
        self.api_url = value.strip()
        self.uploader.set_credentials(self.api_url, self.device_key)

    def api(self) -> ApiClient:
        return ApiClient(self.api_url, self.device_key)

    def send_readings(self, readings, callback=None) -> None:
        self.uploader.submit(readings, callback)

    def test_backend(self) -> tuple[bool, str]:
        if not self.device_key:
            return False, "Enter the machine IoT device key first"
        return self.api().test_connection()

    def disconnect(self) -> None:
        self.serial.disconnect()

    def close(self) -> None:
        self.serial.disconnect()
        self.uploader.stop()
