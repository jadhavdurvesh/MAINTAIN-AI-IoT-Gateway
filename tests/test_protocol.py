from protocol.parser import parse_line
from protocol.validator import validate_readings


def test_parse_sensor_json():
    assert parse_line('{"temperature":29.3,"humidity":67}') == {"temperature":29.3,"humidity":67}


def test_ready_line_is_ignored():
    assert parse_line("MAINTAIN_AI_SENSOR_BRIDGE_READY") is None


def test_validate_sensor_values():
    readings = validate_readings({"temperature":29.3,"humidity":67})
    assert ("temperature", 29.3, "°C") in readings
    assert ("humidity", 67.0, "%") in readings


def test_invalid_temperature_rejected():
    assert validate_readings({"temperature":-9999}) == []
