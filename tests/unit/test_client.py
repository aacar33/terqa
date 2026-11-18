import json

import pytest
import serial

from tab5.client import send_command


def test_ping_command(mock_client_serial):
    """
    Patch tab5.client.serial.Serial.
    Configure the fake device to return the PING JSON response above.
    Call send_command("PING").
    Verify that device.write() was called exactly once with b"PING\n".
    Verify that readline() was called exactly once.
    Verify that the returned result is a dictionary containing exactly the expected command and status.
    Verify the serial connection arguments.
    """
    mock_serial, fake_device = mock_client_serial

    fake_device.readline.return_value = (
         b'{"command":"PING","status":"ok"}\n'
        )

    response = send_command("PING")

    fake_device.write.assert_called_once_with(b"PING\n")

    assert fake_device.readline.call_count == 1

    expected = {'command': 'PING', 'status': 'ok'}

    assert isinstance(response, dict)
    assert response == expected

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)


def test_get_info(mock_client_serial):
    mock_serial, fake_device = mock_client_serial

    fake_device.readline.return_value = (
        b'{"command":"GET_INFO","status":"ok","device":"M5Stack Tab5","firmware":"1.0.0","protocol":1,"sensor":"SCD40"}\n'
    )

    response = send_command("GET_INFO")

    fake_device.write.assert_called_once_with(b"GET_INFO\n")

    assert fake_device.readline.call_count == 1

    expected = {'command': 'GET_INFO',
                'status': 'ok',
                'device': 'M5Stack Tab5',
                'firmware': '1.0.0',
                'protocol': 1,
                'sensor': 'SCD40'
                }

    assert isinstance(response, dict)
    assert response == expected

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)


def test_get_sensor(mock_client_serial):
    mock_serial, fake_device = mock_client_serial

    fake_device.readline.return_value = (
        b'{"command":"GET_SENSOR","status":"ok","co2":1101,"temperature":22.19,"humidity":52.99,"age_ms":1937}\n'
        )

    response = send_command("GET_SENSOR")

    fake_device.write.assert_called_once_with(b"GET_SENSOR\n")

    assert fake_device.readline.call_count == 1

    expected = {'command': 'GET_SENSOR',
                'status': 'ok',
                'co2': 1101,
                'temperature': 22.19,
                'humidity': 52.99,
                'age_ms': 1937
                }

    assert isinstance(response, dict)
    assert isinstance(response["co2"], int)
    assert isinstance(response["temperature"], float)
    assert isinstance(response["humidity"], float)
    assert isinstance(response["age_ms"], int)
    assert response == expected

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)


def test_invalid_json_response(mock_client_serial):
    mock_serial, fake_device = mock_client_serial

    fake_device.readline.return_value = (
        b'INVALID JSON\n'
        )

    with pytest.raises(json.JSONDecodeError):
        send_command("PING")

    fake_device.write.assert_called_once_with(b"PING\n")

    assert fake_device.readline.call_count == 1

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)


def test_no_response_timeout(mock_client_serial):
    mock_serial, fake_device = mock_client_serial

    fake_device.readline.return_value = (
        b''
    )

    with pytest.raises(TimeoutError, match="No response from device"):
        send_command("PING")

    fake_device.write.assert_called_once_with(b"PING\n")

    assert fake_device.readline.call_count == 1

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)


def test_sensor_not_ready(mock_client_serial):
    mock_serial, fake_device = mock_client_serial

    response_data = (
        b'{"command":"GET_SENSOR","status":"error",'
        b'"error":"SENSOR_NOT_READY"}\n'
    )

    fake_device.readline.return_value = response_data

    response = send_command("GET_SENSOR")

    fake_device.write.assert_called_once_with(b"GET_SENSOR\n")

    assert fake_device.readline.call_count == 1

    expected = {
        "command": "GET_SENSOR",
        "status": "error",
        "error": "SENSOR_NOT_READY",
        }

    assert isinstance(response, dict)
    assert response == expected

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)


def test_mismatched_response_command(mock_client_serial):
    mock_serial, fake_device = mock_client_serial

    response_data = b'{"command":"PING","status":"ok"}\n'

    fake_device.readline.return_value = response_data

    with pytest.raises(ValueError, match="Unexpected response command"):
        send_command("GET_SENSOR")

    fake_device.write.assert_called_once_with(b"GET_SENSOR\n")

    assert fake_device.readline.call_count == 1

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)


def test_missing_response_command(mock_client_serial):
    mock_serial, fake_device = mock_client_serial

    response_data = b'{"status":"ok"}\n'

    fake_device.readline.return_value = response_data

    with pytest.raises(ValueError, match="Response does not contain a command key"):
        send_command("GET_SENSOR")

    fake_device.write.assert_called_once_with(b"GET_SENSOR\n")

    assert fake_device.readline.call_count == 1

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)

@pytest.mark.parametrize(
    "response_data",
    [
        b'["PING", "ok"]\n',
        b'"PING"\n',
        b'42\n',
        b'3.14\n',
        b'true\n',
        b'null\n',
    ],
    ids=["list", "string", "integer", "float", "boolean", "null"],
)

def test_invalid_response_structure(mock_client_serial, response_data):
    mock_serial, fake_device = mock_client_serial

    fake_device.readline.return_value = response_data

    with pytest.raises(ValueError, match="Response must be a JSON object"):
        send_command("PING")

    fake_device.write.assert_called_once_with(b"PING\n")

    assert fake_device.readline.call_count == 1

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)


def test_serial_connection_failure(mock_client_serial):
    mock_serial, fake_device = mock_client_serial

    mock_serial.side_effect = serial.SerialException("Serial connection failed")

    with pytest.raises(ConnectionError, match="^Serial communication failed$") as exc_info:
        send_command("PING")

    assert str(exc_info.value.__cause__) == "Serial connection failed"

    assert isinstance(exc_info.value.__cause__, serial.SerialException)

    fake_device.readline.assert_not_called()

    fake_device.write.assert_not_called()

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)


def test_serial_write_failure(mock_client_serial):
    mock_serial, fake_device = mock_client_serial

    fake_device.write.side_effect = serial.SerialException("Serial write failed")

    with pytest.raises(ConnectionError, match="^Serial communication failed$") as exc_info:
        send_command("PING")

    assert str(exc_info.value.__cause__) == "Serial write failed"

    assert isinstance(exc_info.value.__cause__, serial.SerialException)

    fake_device.write.assert_called_once_with(b"PING\n")

    fake_device.readline.assert_not_called()

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)


def test_serial_read_failure(mock_client_serial):
    mock_serial, fake_device = mock_client_serial

    fake_device.readline.side_effect = serial.SerialException("Serial read failed")

    with pytest.raises(ConnectionError, match="^Serial communication failed$") as exc_info:
        send_command("PING")

    assert str(exc_info.value.__cause__) == "Serial read failed"

    assert isinstance(exc_info.value.__cause__, serial.SerialException)

    fake_device.write.assert_called_once_with(b"PING\n")

    fake_device.readline.assert_called_once()

    mock_serial.assert_called_once_with("COM3", 115200, timeout=2)
