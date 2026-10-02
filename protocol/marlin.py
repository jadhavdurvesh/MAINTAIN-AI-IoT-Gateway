import re
from typing import Any


_NUMBER = r"-?(?:\d+(?:\.\d*)?|\.\d+)"
_TEMP_FIELD_RE = re.compile(
    rf"(?P<name>T|B)\s*:\s*(?P<value>{_NUMBER})"
    rf"(?:\s*/\s*{_NUMBER})?",
    re.IGNORECASE,
)
_POSITION_FIELD_RE = re.compile(
    rf"\b(?P<name>[XYZ])\s*:\s*(?P<value>{_NUMBER})",
    re.IGNORECASE,
)


def parse_temperature_report(line: str) -> dict[str, Any] | None:
    """Convert a Marlin M105 temperature report into Maintain AI telemetry."""
    text = line.strip()
    if not text:
        return None

    readings: dict[str, float] = {}
    for match in _TEMP_FIELD_RE.finditer(text):
        name = match.group("name").upper()
        value = float(match.group("value"))
        if name == "T":
            readings["nozzle_temperature"] = value
        elif name == "B":
            readings["bed_temperature"] = value

    return readings or None


def parse_position_report(line: str) -> dict[str, Any] | None:
    """Convert a Marlin M114 position report into X/Y/Z telemetry.

    M114 may include additional fields such as E and duplicate axis values
    in a trailing Count section. The first X/Y/Z occurrence is the primary
    tool position and is therefore retained.
    """
    text = line.strip()
    if not text:
        return None

    readings: dict[str, float] = {}
    names = {"X": "x_position", "Y": "y_position", "Z": "z_position"}
    for match in _POSITION_FIELD_RE.finditer(text):
        axis = match.group("name").upper()
        if axis in {key.upper() for key in names if names[key] in readings}:
            continue
        readings[names[axis]] = float(match.group("value"))

    return readings or None


def is_marlin_line(line: str) -> bool:
    """Return True when a serial line contains a supported Marlin report."""
    return parse_temperature_report(line) is not None or parse_position_report(line) is not None
