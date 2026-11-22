from unittest.mock import patch

import pytest
import serial

from terqa.transports.serial import SerialTransport


def test_get_settings():
    transport = SerialTransport(
        port="COM9",
        baudrate=9600,
        timeout=1,
    )

    assert transport.get_settings() == {
        "port": "COM9",
        "baudrate": 9600,
        "timeout": 1,
    }

    transport2 = SerialTransport(
        port="COM5",
        baudrate=115200,
        timeout=5,
    )

    assert transport2.get_settings() == {
        "port": "COM5",
        "baudrate": 115200,
        "timeout": 5,
    }

    assert transport.get_settings() == {
        "port": "COM9",
        "baudrate": 9600,
        "timeout": 1,
    }


def test_enter_returns_self():
    with patch("terqa.transports.serial.serial.Serial"):
        transport = SerialTransport("COM9", 9600, 1)

        with transport as connection:
            assert connection is transport


def test_context_manager():
    with patch("terqa.transports.serial.serial.Serial"):
        transport = SerialTransport("COM9", 9600, 1)

        with transport as connection:
            assert connection is transport

        assert transport.get_settings()["port"] == "COM9"


def test_context_manager_does_not_suppress_exceptions():
    transport = SerialTransport("COM9", 9600, 1)

    with patch("terqa.transports.serial.serial.Serial"):
        with pytest.raises(ValueError, match="Test failure"):
            with transport:
                raise ValueError("Test failure")


def test_enter_opens_serial_connection():
    with patch("terqa.transports.serial.serial.Serial") as mock_serial:
        transport = SerialTransport("COM9", 9600, 1)

        mock_serial.assert_not_called()

        with transport as connection:
            assert connection is transport

            mock_serial.assert_called_once_with(
                port="COM9",
                baudrate=9600,
                timeout=1,
            )


def test_exit_closes_serial_connection():
    with patch("terqa.transports.serial.serial.Serial") as mock_serial:
        transport = SerialTransport("COM9", 9600, 1)

        with transport:
            mock_serial.return_value.close.assert_not_called()

        mock_serial.return_value.close.assert_called_once_with()


def test_exit_closes_connection_on_exception():
    with patch("terqa.transports.serial.serial.Serial") as mock_serial:
        transport = SerialTransport("COM9", 9600, 1)

        with pytest.raises(ValueError, match="Test failure"):
            with transport:
                raise ValueError("Test failure")

        mock_serial.return_value.close.assert_called_once_with()
        assert transport._connection is None


def test_write_sends_bytes():
    with patch("terqa.transports.serial.serial.Serial") as mock_serial:
        transport = SerialTransport("COM9", 9600, 1)

        with transport:
            transport.write(b"PING\n")

        mock_serial.return_value.write.assert_called_once_with(b"PING\n")


def test_write_without_connection():
    transport = SerialTransport("COM9", 9600, 1)

    with pytest.raises(RuntimeError, match="Serial connection is not open"):
        transport.write(b"PING\n")


def test_readline_returns_bytes():
    with patch("terqa.transports.serial.serial.Serial") as mock_serial:
        fake_device = mock_serial.return_value
        fake_device.readline.return_value = b"HELLO\n"

        transport = SerialTransport("COM9", 9600, 1)

        with transport:
            response = transport.readline()

        assert response == b"HELLO\n"
        fake_device.readline.assert_called_once_with()


def test_readline_without_connection():
    transport = SerialTransport("COM9", 9600, 1)

    with pytest.raises(RuntimeError, match="Serial connection is not open"):
        transport.readline()


def test_serial_connection_open_failure():
    with patch("terqa.transports.serial.serial.Serial") as mock_serial:
        mock_serial.side_effect = serial.SerialException("Unable to open port")

        transport = SerialTransport("COM9", 9600, 1)

        with pytest.raises(serial.SerialException, match="Unable to open port"):
            with transport:
                pass

        mock_serial.assert_called_once_with(port="COM9", baudrate=9600, timeout=1)

        assert transport._connection is None


def test_serial_write_failure():

    with patch("terqa.transports.serial.serial.Serial") as mock_serial:
        transport = SerialTransport("COM9", 9600, 1)

        mock_serial.return_value.write.side_effect = serial.SerialException(
            "Write failed"
        )

        with pytest.raises(serial.SerialException, match="Write failed"):
            with transport:
                transport.write(b"PING\n")

        mock_serial.return_value.write.assert_called_once_with(b"PING\n")

        mock_serial.return_value.close.assert_called_once_with()

        assert transport._connection is None


def test_serial_readline_failure():
    with patch("terqa.transports.serial.serial.Serial") as mock_serial:
        transport = SerialTransport("COM9", 9600, 1)

        mock_serial.return_value.readline.side_effect = serial.SerialException(
            "Read failed"
        )

        with pytest.raises(serial.SerialException, match="Read failed"):
            with transport:
                transport.readline()

        mock_serial.return_value.readline.assert_called_once_with()

        mock_serial.return_value.close.assert_called_once_with()

        assert transport._connection is None


def test_close_failure_resets_connection():
    with patch("terqa.transports.serial.serial.Serial") as mock_serial:
        transport = SerialTransport("COM9", 9600, 1)

        mock_serial.return_value.close.side_effect = serial.SerialException(
            "Close failed"
        )

        with pytest.raises(serial.SerialException, match="Close failed"):
            with transport:
                pass

        mock_serial.return_value.close.assert_called_once_with()

        assert transport._connection is None


def test_enter_when_connection_already_open():
    with patch("terqa.transports.serial.serial.Serial") as mock_serial:
        transport = SerialTransport("COM9", 9600, 1)

        with transport:
            with pytest.raises(RuntimeError, match="Serial connection is already open"):
                with transport:
                    pass

        mock_serial.return_value.close.assert_called_once_with()

        mock_serial.assert_called_once_with(
            port="COM9",
            baudrate=9600,
            timeout=1,
        )

        assert transport._connection is None
