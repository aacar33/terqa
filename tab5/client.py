import json

import serial

from tab5.exceptions import ProtocolError, ResponseTimeoutError, SerialCommunicationError


def send_command(command, port="COM3", baudrate=115200, timeout=2):
    """
    Open a serial connection using the supplied settings.
    Send the command followed by \n.
    Read one response line using readline().
    Decode the response from bytes into a string.
    Parse the JSON using json.loads().
    Return the resulting dictionary.
    Close the connection using a with statement.
    """
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as device:
            device.write((command + "\n").encode("utf-8"))

            response = device.readline()
            message = response.decode("utf-8").strip()

        if message == "":
            raise ResponseTimeoutError("No response from device")

        result = json.loads(message)

        if not isinstance(result, dict):
            raise ProtocolError("Response must be a JSON object")

        if "command" not in result:
            raise ProtocolError("Response does not contain a command key")

        if result["command"] != command:
            raise ProtocolError("Unexpected response command")

    except serial.SerialException as exc:
        raise SerialCommunicationError("Serial communication failed") from exc

    return result
