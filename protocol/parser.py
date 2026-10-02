import json
from typing import Any

from protocol.marlin import parse_temperature_report


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

    # Marlin firmware reports temperatures as plain text, for example:
    # "ok T:28.38 /0.00 B:26.16 /0.00 @:0 B@:0"
    return parse_temperature_report(text)
