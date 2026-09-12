from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class SensorReading:
    reading_type: str
    value: float
    unit: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def payload(self) -> dict[str, Any]:
        return {"reading_type": self.reading_type, "value": self.value, "unit": self.unit}


@dataclass
class SerialDevice:
    port: str
    description: str
    manufacturer: str = ""
    vid: int | None = None
    pid: int | None = None


@dataclass
class GatewaySnapshot:
    serial_connected: bool = False
    backend_connected: bool = False
    machine: str = "Not paired"
    last_readings: dict[str, SensorReading] = field(default_factory=dict)
    last_upload: datetime | None = None
    status: str = "Waiting for connection"
