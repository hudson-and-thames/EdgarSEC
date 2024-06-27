class EdgarClientException(Exception):
    """Base exception for EdgarClient."""
    pass


class InvalidCIKException(EdgarClientException):
    """Exception raised for invalid CIK."""
    pass


class RequestFailedException(EdgarClientException):
    """Exception raised for failed requests."""
    pass
