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


def test_specialized_cnc_and_robot_values_are_preserved():
    readings = validate_readings({
        "spindle_rpm": 6400,
        "spindle_load": 45.5,
        "joint_1": 84.1,
        "base_angle": 12.4,
    })
    assert ("spindle_rpm", 6400.0, "rpm") in readings
    assert ("spindle_load", 45.5, "%") in readings
    assert ("joint_1", 84.1, "°") in readings
    assert ("base_angle", 12.4, "°") in readings


def test_single_reading_device_contract():
    assert validate_readings({"reading_type": "nozzle_temperature", "value": 215.0, "unit": "°C"}) == [("nozzle_temperature", 215.0, "°C")]


def test_future_custom_signal_requires_unit():
    assert validate_readings({"custom_sensor": {"value": 12.5, "unit": "kPa"}}) == [("custom_sensor", 12.5, "kPa")]
    assert validate_readings({"custom_sensor": 12.5}) == []
