from enum import Enum


class HttpMethod(Enum):
    """An enum representing HTTP methods."""
    GET = "GET"
    POST = "POST"


class HttpStatusCode(Enum):
    """An enum representing HTTP status code."""
    OK = (200, "OK")
    NOT_FOUND = (404, "Not Found")
    CREATED = (201, "Created")


class RequestLine:
    """A representation of the request line"""

    def __init__(self, method: HttpMethod, path: str, http_version: str) -> None:
        self.method = method
        self.path = path
        self.http_version = http_version
