import serial


class SerialTransport:
    def __init__(self, port, baudrate, timeout):
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._connection = None

    def __enter__(self):
        self._connection = serial.Serial(
            port=self._port, baudrate=self._baudrate, timeout=self._timeout
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._connection is not None:
            self._connection.close()
            self._connection = None

    def get_settings(self):
        return {
            "port": self._port,
            "baudrate": self._baudrate,
            "timeout": self._timeout,
        }

    def write(self, data):
        if self._connection is None:
            raise RuntimeError("Serial connection is not open")

        return self._connection.write(data)

    def readline(self):
        if self._connection is None:
            raise RuntimeError("Serial connection is not open")

        return self._connection.readline()
