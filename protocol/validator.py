import re
from typing import Any

# Canonical MAINTAIN AI signal catalog. Specialized machine signals are
# intentionally included here so the physical gateway can forward CNC, robot,
# hydraulic, packaging, and 3D-printer telemetry without renaming it.
SIGNALS: dict[str, tuple[str, float, float]] = {
    "temperature": ("°C", -100.0, 300.0),
    "humidity": ("%", 0.0, 100.0),
    "vibration": ("g", 0.0, 1_000_000.0),
    "current": ("A", 0.0, 1_000_000.0),
    "voltage": ("V", 0.0, 1_000_000.0),
    "pressure": ("Pa", 0.0, 1_000_000.0),
    "flow": ("L/min", 0.0, 1_000_000.0),
    "speed": ("m/s", 0.0, 1_000_000.0),
    "load": ("%", 0.0, 1_000_000.0),
    "rpm": ("rpm", 0.0, 10_000_000.0),
    "distance": ("mm", -1_000_000.0, 1_000_000.0),
    # CNC / machining
    "spindle_rpm": ("rpm", 0.0, 10_000_000.0),
    "spindle_load": ("%", 0.0, 100.0),
    "spindle_temperature": ("°C", -100.0, 300.0),
    "spindle_vibration": ("g", 0.0, 1_000_000.0),
    "spindle_current": ("A", 0.0, 1_000_000.0),
    "tool_life": ("%", 0.0, 100.0),
    "coolant_temperature": ("°C", -100.0, 300.0),
    "coolant_flow": ("L/min", 0.0, 1_000_000.0),
    "x_position": ("mm", -1_000_000.0, 1_000_000.0),
    "y_position": ("mm", -1_000_000.0, 1_000_000.0),
    "z_position": ("mm", -1_000_000.0, 1_000_000.0),
    "x_velocity": ("mm/s", -1_000_000.0, 1_000_000.0),
    "y_velocity": ("mm/s", -1_000_000.0, 1_000_000.0),
    "z_velocity": ("mm/s", -1_000_000.0, 1_000_000.0),
    "x_current": ("A", 0.0, 1_000_000.0),
    "y_current": ("A", 0.0, 1_000_000.0),
    "z_current": ("A", 0.0, 1_000_000.0),
    # Industrial robot
    "base_angle": ("°", -360.0, 360.0),
    "radial_position": ("mm", -1_000_000.0, 1_000_000.0),
    "vertical_position": ("mm", -1_000_000.0, 1_000_000.0),
    "base_current": ("A", 0.0, 1_000_000.0),
    "radial_current": ("A", 0.0, 1_000_000.0),
    "vertical_current": ("A", 0.0, 1_000_000.0),
    "joint_1": ("°", -360.0, 360.0),
    "joint_2": ("°", -360.0, 360.0),
    "joint_3": ("°", -360.0, 360.0),
    "joint_4": ("°", -360.0, 360.0),
    "joint_5": ("°", -360.0, 360.0),
    "joint_6": ("°", -360.0, 360.0),
    "joint_1_position": ("°", -360.0, 360.0),
    "joint_2_position": ("°", -360.0, 360.0),
    "joint_3_position": ("°", -360.0, 360.0),
    "joint_4_position": ("°", -360.0, 360.0),
    "joint_5_position": ("°", -360.0, 360.0),
    "joint_6_position": ("°", -360.0, 360.0),
    "joint_torque": ("Nm", -1_000_000.0, 1_000_000.0),
    "motor_current": ("A", 0.0, 1_000_000.0),
    "motor_load": ("%", 0.0, 100.0),
    "motor_temperature": ("°C", -100.0, 300.0),
    "external_force": ("N", 0.0, 1_000_000.0),
    "tcp_speed": ("mm/s", 0.0, 1_000_000.0),
    # 3D printer
    "nozzle_temperature": ("°C", -50.0, 500.0),
    "bed_temperature": ("°C", -50.0, 300.0),
    "chamber_temperature": ("°C", -50.0, 300.0),
    "hotend_current": ("A", 0.0, 1_000_000.0),
    "fan_speed": ("%", 0.0, 100.0),
    "print_speed": ("mm/s", 0.0, 1_000_000.0),
    "extrusion_rate": ("mm³/s", 0.0, 1_000_000.0),
    "print_progress": ("%", 0.0, 100.0),
    # General industrial profiles
    "hydraulic_pressure": ("Pa", 0.0, 1_000_000_000.0),
    "injection_pressure": ("Pa", 0.0, 1_000_000_000.0),
    "steam_pressure": ("Pa", 0.0, 1_000_000_000.0),
    "flow_rate": ("L/min", 0.0, 1_000_000.0),
    "level": ("%", 0.0, 100.0),
    "utilization": ("%", 0.0, 100.0),
}

# Backwards-compatible exports used by older integrations/tests.
RANGES = {name: (low, high) for name, (_, low, high) in SIGNALS.items()}
UNITS = {name: unit for name, (unit, _, _) in SIGNALS.items()}
_NAME_RE = re.compile(r"^[a-z][a-z0-9_]{1,63}$")


def _coerce_reading(name: str, raw: Any) -> tuple[float, str] | None:
    unit = None
    value = raw
    if isinstance(raw, dict):
        value = raw.get("value")
        unit = raw.get("unit")
    if isinstance(value, bool):
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    if not _NAME_RE.fullmatch(name):
        return None

    if name in SIGNALS:
        default_unit, low, high = SIGNALS[name]
        if not low <= numeric <= high:
            return None
        return numeric, str(unit or default_unit)

    # Allow future machine-specific sensors without requiring a gateway release.
    # Unknown names still need a safe numeric range and a supplied unit.
    if unit is None or not isinstance(unit, str) or not unit.strip():
        return None
    if abs(numeric) > 1_000_000_000:
        return None
    return numeric, unit.strip()[:24]


def validate_readings(payload: dict[str, Any]) -> list[tuple[str, float, str]]:
    if not isinstance(payload, dict):
        return []
    source = payload.get("readings") if isinstance(payload.get("readings"), dict) else payload
    results: list[tuple[str, float, str]] = []
    for name, raw in source.items():
        if name in {"event_id", "recorded_at", "device_id", "machine_id", "timestamp", "reading_type", "value", "unit"}:
            continue
        coerced = _coerce_reading(str(name), raw)
        if coerced is not None:
            value, unit = coerced
            results.append((str(name), value, unit))

    # Also accept the single-reading device contract directly.
    if not results and isinstance(payload.get("reading_type"), str) and "value" in payload:
        name = payload["reading_type"].strip()
        coerced = _coerce_reading(name, {"value": payload.get("value"), "unit": payload.get("unit")})
        if coerced is not None:
            value, unit = coerced
            results.append((name, value, unit))
    return results
