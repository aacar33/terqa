import pytest

from tab5.parser import parse_sensor_message


def test_valid_reading():
    message = "CO2: 936 ppm | Temp: 23.35 C | Humidity: 55.24 %"

    expected = {
        "CO2": 936,
        "Temp": 23.35,
        "Humidity": 55.24,
    }

    assert parse_sensor_message(message) == expected


def test_invalid_reading():
    message = "CO2: INVALID ppm | Temp: 23.35 C | Humidity: 55.24 %"

    with pytest.raises(ValueError):
        parse_sensor_message(message)


def test_missing_reading():
    message = "CO2: 936 ppm | Temp: 23.35 C"

    with pytest.raises(ValueError):
        parse_sensor_message(message)


def test_unexpected_reading():
    message = "CO2: 936 ppm | Temp: 23.35 C | Pressure: 55.24 %"

    with pytest.raises(ValueError):
        parse_sensor_message(message)


def test_no_readings():
    with pytest.raises(ValueError):
        parse_sensor_message("")
