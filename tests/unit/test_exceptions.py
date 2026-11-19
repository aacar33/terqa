from tab5.exceptions import (
    ProtocolError,
    ResponseTimeoutError,
    SerialCommunicationError,
    TERQAError,
)


def test_terqa_error_inheritance():
    """Verify inheritance from Exception."""

    error = TERQAError("Error message")
    assert isinstance(error, Exception)
    assert issubclass(TERQAError, Exception)


def test_terqa_error_message():
    """Verify message preservation when instantiating TERQAError."""

    message = "TERQA error message."
    error = TERQAError(message)
    assert str(error) == message


def test_serial_communication_error_inheritance():
    """Verify that SerialCommunicationError is a subclass of TERQAError and
    that an instance belongs to both ConnectionError and TERQAError."""

    error = SerialCommunicationError("Serial communication failed")
    assert isinstance(error, ConnectionError)
    assert isinstance(error, TERQAError)
    assert issubclass(SerialCommunicationError, ConnectionError)
    assert issubclass(SerialCommunicationError, TERQAError)
    assert str(error) == "Serial communication failed"


def test_response_timeout_error_inheritance():
    """Verify that ResponseTimeoutError is a subclass of TERQAError and
    that an instance belongs to both TimeoutError and TERQAError."""

    error = ResponseTimeoutError("Response timed out")
    assert isinstance(error, TimeoutError)
    assert isinstance(error, TERQAError)
    assert issubclass(ResponseTimeoutError, TimeoutError)
    assert issubclass(ResponseTimeoutError, TERQAError)
    assert str(error) == "Response timed out"


def test_protocol_error_inheritance():
    """Verify that ProtocolError is a subclass of TERQAError and
    that an instance belongs to both ValueError and TERQAError."""

    error = ProtocolError("Protocol error occurred")
    assert isinstance(error, ValueError)
    assert isinstance(error, TERQAError)
    assert issubclass(ProtocolError, ValueError)
    assert issubclass(ProtocolError, TERQAError)
    assert str(error) == "Protocol error occurred"
