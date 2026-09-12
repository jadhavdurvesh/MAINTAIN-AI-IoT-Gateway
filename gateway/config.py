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
        return {"api_url": os.getenv("MAINTAIN_AI_API_URL", DEFAULT_API_URL), "baud_rate": DEFAULT_BAUD_RATE, "port": ""}
    try:
        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        data = {}
    data.setdefault("api_url", DEFAULT_API_URL)
    data.setdefault("baud_rate", DEFAULT_BAUD_RATE)
    data.setdefault("port", "")
    return data


def save_config(data: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_device_key() -> str:
    return keyring.get_password(SERVICE_NAME, "device_key") or ""


def set_device_key(value: str) -> None:
    if value:
        keyring.set_password(SERVICE_NAME, "device_key", value)
    else:
        try:
            keyring.delete_password(SERVICE_NAME, "device_key")
        except keyring.errors.PasswordDeleteError:
            pass
