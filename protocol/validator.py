from typing import Any

RANGES = {
    "temperature": (-100.0, 200.0),
    "humidity": (0.0, 100.0),
    "vibration": (0.0, 1_000_000.0),
    "current": (0.0, 1_000_000.0),
    "voltage": (0.0, 1_000_000.0),
    "pressure": (0.0, 1_000_000.0),
    "flow": (0.0, 1_000_000.0),
    "speed": (0.0, 1_000_000.0),
    "load": (0.0, 1_000_000.0),
    "rpm": (0.0, 10_000_000.0),
    "distance": (0.0, 1_000_000.0),
}
UNITS = {"temperature": "°C", "humidity": "%", "vibration": "g", "current": "A", "voltage": "V", "pressure": "Pa", "flow": "L/min", "speed": "m/s", "load": "N", "rpm": "rpm", "distance": "mm"}


def validate_readings(payload: dict[str, Any]) -> list[tuple[str, float, str]]:
    source = payload.get("readings") if isinstance(payload.get("readings"), dict) else payload
    results: list[tuple[str, float, str]] = []
    for name, raw in source.items():
        if name not in UNITS or isinstance(raw, bool):
            continue
        try:
            value = float(raw)
        except (TypeError, ValueError):
            continue
        low, high = RANGES[name]
        if low <= value <= high:
            results.append((name, value, UNITS[name]))
    return results
