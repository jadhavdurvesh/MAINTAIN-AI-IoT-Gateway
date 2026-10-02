import json
from typing import Any

from protocol.marlin import parse_position_report, parse_temperature_report


def parse_line(line: str) -> dict[str, Any] | None:
    text = line.strip()
    if not text or text == "MAINTAIN_AI_SENSOR_BRIDGE_READY":
        return None

    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        payload = None

    if isinstance(payload, dict):
        return payload

    marlin_temperature = parse_temperature_report(text)
    if marlin_temperature is not None:
        return marlin_temperature

    return parse_position_report(text)
