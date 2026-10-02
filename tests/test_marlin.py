from protocol.marlin import parse_temperature_report
from protocol.parser import parse_line
from protocol.validator import validate_readings


def test_parse_marlin_temperature_report():
    payload = parse_temperature_report("ok T:28.38 /200.00 B:26.16 /60.00 @:0 B@:0")
    assert payload == {
        "nozzle_temperature": 28.38,
        "bed_temperature": 26.16,
        "hotend_heater_power": 0.0,
        "bed_heater_power": 0.0,
    }


def test_parse_marlin_line_through_common_parser():
    payload = parse_line("ok T:215.5 /210.0 B:60.2 /60.0")
    assert payload["nozzle_temperature"] == 215.5
    assert payload["bed_temperature"] == 60.2


def test_validate_marlin_readings():
    readings = validate_readings({
        "nozzle_temperature": 215.5,
        "bed_temperature": 60.2,
    })
    assert ("nozzle_temperature", 215.5, "°C") in readings
    assert ("bed_temperature", 60.2, "°C") in readings
