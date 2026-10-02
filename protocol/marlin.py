import re
from typing import Any


# Marlin temperature reports commonly look like:
#   ok T:28.38 /0.00 B:26.16 /0.00 @:0 B@:0
# The parser deliberately accepts optional "ok" / "busy" prefixes and
# additional Marlin fields so firmware variations don't break telemetry.
_FIELD_RE = re.compile(
    r"(?P<name>T|B|C|@|B@)\s*:\s*(?P<value>-?(?:\d+(?:\.\d*)?|\.\d+))"
    r"(?:\s*/\s*-?(?:\d+(?:\.\d*)?|\.\d+))?",
    re.IGNORECASE,
)


def parse_temperature_report(line: str) -> dict[str, Any] | None:
    """Convert a Marlin temperature/status line into gateway telemetry JSON."""
    text = line.strip()
    if not text:
        return None

    matches = list(_FIELD_RE.finditer(text))
    if not matches:
        return None

    readings: dict[str, float] = {}
    for match in matches:
        name = match.group("name").upper()
        value = float(match.group("value"))
        if name == "T":
            readings["nozzle_temperature"] = value
        elif name == "B":
            readings["bed_temperature"] = value
        elif name == "C":
            readings["chamber_temperature"] = value
        elif name == "@":
            readings["hotend_heater_power"] = value
        elif name == "B@":
            readings["bed_heater_power"] = value

    return readings or None


def is_marlin_line(line: str) -> bool:
    """Return True when a serial line contains a recognizable Marlin report."""
    return parse_temperature_report(line) is not None
