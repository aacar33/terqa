class TERQAError(Exception):
    """Base class for all TERQA-related exceptions."""


class SerialCommunicationError(ConnectionError, TERQAError):
    """Custom exception for serial communication errors."""


class ResponseTimeoutError(TimeoutError, TERQAError):
    """Custom exception for response timeouts."""


class ProtocolError(ValueError, TERQAError):
    """Custom exception for protocol errors."""
