from protocol.marlin import parse_position_report, parse_temperature_report
from protocol.parser import parse_line
from protocol.validator import validate_readings


def test_parse_marlin_temperature_report():
    payload = parse_temperature_report("ok T:28.38 /200.00 B:26.16 /60.00 @:0 B@:0")
    assert payload == {
        "nozzle_temperature": 28.38,
        "bed_temperature": 26.16,
    }


def test_parse_marlin_position_report():
    payload = parse_position_report(
        "X:125.40 Y:87.20 Z:3.20 E:15.42 Count X:10000 Y:7000 Z:320"
    )
    assert payload == {
        "x_position": 125.40,
        "y_position": 87.20,
        "z_position": 3.20,
    }


def test_parse_marlin_line_through_common_parser():
    temperature = parse_line("ok T:215.5 /210.0 B:60.2 /60.0")
    position = parse_line("X:125.4 Y:87.2 Z:3.2 E:15.4")
    assert temperature["nozzle_temperature"] == 215.5
    assert temperature["bed_temperature"] == 60.2
    assert position["x_position"] == 125.4
    assert position["y_position"] == 87.2
    assert position["z_position"] == 3.2


def test_validate_marlin_readings():
    readings = validate_readings({
        "nozzle_temperature": 215.5,
        "bed_temperature": 60.2,
        "x_position": 125.4,
        "y_position": 87.2,
        "z_position": 3.2,
    })
    assert ("nozzle_temperature", 215.5, "°C") in readings
    assert ("bed_temperature", 60.2, "°C") in readings
    assert ("x_position", 125.4, "mm") in readings
    assert ("y_position", 87.2, "mm") in readings
    assert ("z_position", 3.2, "mm") in readings
