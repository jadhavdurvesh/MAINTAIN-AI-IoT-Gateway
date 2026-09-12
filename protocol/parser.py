import json
from typing import Any


def parse_line(line: str) -> dict[str, Any] | None:
    text = line.strip()
    if not text or text == "MAINTAIN_AI_SENSOR_BRIDGE_READY":
        return None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return None
    return payload if isinstance(payload, dict) else None
