import json
import os
from pathlib import Path

import keyring

APP_NAME = "MAINTAIN AI IoT Gateway"
SERVICE_NAME = "maintain-ai-iot-gateway"
DEFAULT_API_URL = "https://maintain-ai-3.vercel.app/api/devices/ingest"
DEFAULT_BAUD_RATE = 115200
CONFIG_DIR = Path.home() / ".maintain-ai-iot-gateway"
CONFIG_FILE = CONFIG_DIR / "config.json"


def load_config() -> dict:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not CONFIG_FILE.exists():
        return {"api_url": os.getenv("MAINTAIN_AI_API_URL", DEFAULT_API_URL), "baud_rate": DEFAULT_BAUD_RATE, "devices": []}
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    data.setdefault("api_url", DEFAULT_API_URL)
    data.setdefault("baud_rate", DEFAULT_BAUD_RATE)
    devices = data.setdefault("devices", [])
    if not isinstance(devices, list):
        data["devices"] = []
    # Migrate the original single-device configuration if it exists.
    if not data["devices"] and data.get("port"):
        data["devices"] = [{
            "id": "device-1",
            "name": "Device 01",
            "machine": "",
            "port": data["port"],
            "baud_rate": data.get("baud_rate", DEFAULT_BAUD_RATE),
        }]
    return data


def save_config(data: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_device_key(device_id: str = "default") -> str:
    return keyring.get_password(SERVICE_NAME, f"device:{device_id}") or ""


def set_device_key(device_id: str, value: str) -> None:
    if value:
        keyring.set_password(SERVICE_NAME, f"device:{device_id}", value)
    else:
        try:
            keyring.delete_password(SERVICE_NAME, f"device:{device_id}")
        except keyring.errors.PasswordDeleteError:
            pass


def delete_device_key(device_id: str) -> None:
    set_device_key(device_id, "")
