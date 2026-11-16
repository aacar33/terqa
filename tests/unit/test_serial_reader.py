from unittest.mock import patch

import pytest

from tab5.serial_reader import read_device


def test_read_five_measurements(capsys):
    with patch("tab5.serial_reader.serial.Serial") as mock_serial:
        # Obtain the fake device
        fake_device = mock_serial.return_value.__enter__.return_value

        # Configure the fake device's readline() response
        fake_device.readline.return_value = (
            b"CO2: 775 ppm | Temp: 24.46 C | Humidity: 46.44 %\n"
        )

        # Execute the real read_device() function
        read_device()

        captured = capsys.readouterr()
        output = captured.out
        lines = output.splitlines()

        assert len(lines) == 5

        expected = "{'CO2': 775, 'Temp': 24.46, 'Humidity': 46.44}"

        assert all(line == expected for line in lines)

        # Assert the number of readline() calls
        assert fake_device.readline.call_count == 5

        # Assert the serial connection arguments
        mock_serial.assert_called_once_with("COM3", 115200, timeout=10)

def test_read_changing_measurements(capsys):
    """
    Patch tab5.serial_reader.serial.Serial.
    Obtain the fake device using the context-manager expression.
    Configure readline.side_effect with the five measurements above.
    Call the real read_device().
    Capture its output using capsys.
    Verify that exactly five lines were printed.
    Verify that each line contains the correct parsed dictionary, in the order.
    Verify that readline() was called exactly five times.
    """
    readings = [
        b"CO2: 775 ppm | Temp: 24.46 C | Humidity: 46.44 %\n",
        b"CO2: 770 ppm | Temp: 24.25 C | Humidity: 47.06 %\n",
        b"CO2: 773 ppm | Temp: 24.04 C | Humidity: 47.62 %\n",
        b"CO2: 777 ppm | Temp: 23.84 C | Humidity: 48.14 %\n",
        b"CO2: 778 ppm | Temp: 23.68 C | Humidity: 48.66 %\n",
    ]

    with patch("tab5.serial_reader.serial.Serial") as mock_serial:
        fake_device = mock_serial.return_value.__enter__.return_value

        fake_device.readline.side_effect = readings

        read_device()

        assert fake_device.readline.call_count == 5

        captured = capsys.readouterr()
        output = captured.out
        lines = output.splitlines()

        assert len(lines) == 5

        expected = [
            "{'CO2': 775, 'Temp': 24.46, 'Humidity': 46.44}",
            "{'CO2': 770, 'Temp': 24.25, 'Humidity': 47.06}",
            "{'CO2': 773, 'Temp': 24.04, 'Humidity': 47.62}",
            "{'CO2': 777, 'Temp': 23.84, 'Humidity': 48.14}",
            "{'CO2': 778, 'Temp': 23.68, 'Humidity': 48.66}",
        ]

        assert lines == expected


def test_invalid_sensor_message():
    with patch("tab5.serial_reader.serial.Serial") as mock_serial:
        fake_device = mock_serial.return_value.__enter__.return_value

        invalid_message = (
            b"CO2: INVALID ppm | Temp: 24.46 C | Humidity: 46.44 %\n"
        )

        fake_device.readline.return_value = invalid_message

        with pytest.raises(ValueError):
            read_device()

        assert fake_device.readline.call_count == 1


def test_skip_invalid_sensor_message(capsys):
    with patch("tab5.serial_reader.serial.Serial") as mock_serial:
        fake_device = mock_serial.return_value.__enter__.return_value

        readings = [
            b"CO2: INVALID ppm | Temp: 24.46 C | Humidity: 46.44 %\n",
            b"CO2: 775 ppm | Temp: 24.46 C | Humidity: 46.44 %\n",
            b"CO2: 770 ppm | Temp: 24.25 C | Humidity: 47.06 %\n",
            b"CO2: 773 ppm | Temp: 24.04 C | Humidity: 47.62 %\n",
            b"CO2: 777 ppm | Temp: 23.84 C | Humidity: 48.14 %\n",
            b"CO2: 778 ppm | Temp: 23.68 C | Humidity: 48.66 %\n",
        ]

        fake_device.readline.side_effect = readings

        read_device(skip_invalid=True)

        assert fake_device.readline.call_count == 6

        captured = capsys.readouterr()
        output = captured.out
        lines = output.splitlines()

        assert lines[0].startswith("Invalid sensor message:")

        assert len(lines) == 6

        valid_lines = lines[1:]

        valid_expected = [
            "{'CO2': 775, 'Temp': 24.46, 'Humidity': 46.44}",
            "{'CO2': 770, 'Temp': 24.25, 'Humidity': 47.06}",
            "{'CO2': 773, 'Temp': 24.04, 'Humidity': 47.62}",
            "{'CO2': 777, 'Temp': 23.84, 'Humidity': 48.14}",
            "{'CO2': 778, 'Temp': 23.68, 'Humidity': 48.66}",
        ]

        assert valid_lines == valid_expected


def test_returned_measurements(capsys):
    with patch("tab5.serial_reader.serial.Serial") as mock_serial:
        fake_device = mock_serial.return_value.__enter__.return_value

        fake_device.readline.return_value = (
            b"CO2: 775 ppm | Temp: 24.46 C | Humidity: 46.44 %\n"
        )

        results = read_device()

        assert len(results) == 5
        assert isinstance(results, list)

        captured = capsys.readouterr()
        output = captured.out
        lines = output.splitlines()

        assert len(lines) == 5
        assert fake_device.readline.call_count == 5
        assert all(result["CO2"] == 775 for result in results)
        assert all(result["Temp"] == 24.46 for result in results)
        assert all(result["Humidity"] == 46.44 for result in results)


def test_read_measurements_without_printing(capsys):
    with patch("tab5.serial_reader.serial.Serial") as mock_serial:
        fake_device = mock_serial.return_value.__enter__.return_value

        fake_device.readline.return_value = (
            b"CO2: 775 ppm | Temp: 24.46 C | Humidity: 46.44 %\n"
        )

        results = read_device(verbose=False)

        assert len(results) == 5
        assert isinstance(results, list)

        assert fake_device.readline.call_count == 5
        assert all(result["CO2"] == 775 for result in results)
        assert all(result["Temp"] == 24.46 for result in results)
        assert all(result["Humidity"] == 46.44 for result in results)

        captured = capsys.readouterr()
        assert captured.out == ""

def test_custom_serial_settings():
    with patch("tab5.serial_reader.serial.Serial") as mock_serial:
        fake_device = mock_serial.return_value.__enter__.return_value

        fake_device.readline.return_value = (
            b"CO2: 775 ppm | Temp: 24.46 C | Humidity: 46.44 %\n"
        )

        read_device(
                    port="COM5",
                    baudrate=9600,
                    serial_timeout=2,
                    verbose=False,
        )

        assert fake_device.readline.call_count == 5

        mock_serial.assert_called_once_with("COM5", 9600, timeout=2)
