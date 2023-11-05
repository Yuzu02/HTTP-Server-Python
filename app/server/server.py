from app.constants.constants import CRLF, END_HEADERS
from app.server.types import HttpMethod, HttpStatusCode, RequestLine


class Request:
    """Request parser"""

    def __init__(self, data: bytes) -> None:
        data: list[str] = data.decode().splitlines().copy()
        method, self.path, self.http_version = data[0].split(' ')
        data.pop(0)
        self.method = HttpMethod(method)
        self.headers = {}
        self.body = data[-1]
        for header in data:
            if header == '':
                break
            key, value = header.split(': ')
            self.headers[key] = value

    def get_request_line(self) -> RequestLine:
        return RequestLine(self.method, self.path, self.http_version)


class Response:
    """Response parser"""

    def __init__(
        self,
        request: Request,
        code: HttpStatusCode,
        headers: dict = {},
        body: str = ""
    ) -> None:
        self.rq = request.get_request_line()
        self.code = code
        self.headers = headers
        self.body = body

    def encode(self) -> bytes:
        message = f"{self.rq.http_version} {self.code.value[0]} {self.code.value[1]}"
        for header in self.headers:
            message += f"{CRLF}{header}: {self.headers[header]}"
        message += END_HEADERS + self.body
        return message.encode()
