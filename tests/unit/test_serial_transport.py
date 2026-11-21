from unittest.mock import patch

import pytest

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
