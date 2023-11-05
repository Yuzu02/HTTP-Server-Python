"""A simple HTTP server."""
import socket
import threading
from enum import Enum

HOST = "localhost"
PORT = 4221
BUFFER_ZISE = 1024
CRLF = '\r\n'
END_HEADERS = CRLF + CRLF


class HttpMethod(Enum):
    """An enum representing HTTP methods."""
    GET = "GET"


class HttpStatusCode(Enum):

    OK = (200, "OK")
    NOT_FOUND = (404, "Not Found")


class RequestLine:
    def __init__(self, method: HttpMethod, path: str, http_version: str) -> None:
        self.method = method
        self.path = path
        self.http_version = http_version


class Request:
    def __init__(self, data: bytes) -> None:
        data: list[str] = data.decode().splitlines().copy()
        method, path, http_version = data[0].split(' ')
        data.pop(0)
        self.method = HttpMethod(method)
        self.path = path
        self.http_version = http_version
        self.headers = {}
        for header in data:
            if header == '':
                break
            key, value = header.split(': ')
            self.headers[key] = value

    def get_request_line(self) -> RequestLine:
        return RequestLine(self.method, self.path, self.http_version)


class Response:
    def __init__(
        self,
        request_line: RequestLine,
        code: HttpStatusCode,
        headers: dict = {},
        body: str = ""
    ) -> None:
        self.rq = request_line
        self.code = code
        self.headers = headers
        self.body = body

    def encode(self, ):
        message = f"{self.rq.http_version} {self.code.value[0]} {self.code.value[1]}"
        for header in self.headers:
            message += f"{CRLF}{header}: {self.headers[header]}"
        message += END_HEADERS + self.body
        return message.encode()


def client_handler(conn):
    data = conn.recv(BUFFER_ZISE)
    request = Request(data)

    if request.path == '/':
        response = Response(request.get_request_line(), HttpStatusCode.OK)
    elif request.path.startswith('/echo/'):
        message = request.path.split('/echo/')[1]
        response = Response(
            request.get_request_line(),
            HttpStatusCode.OK,
            headers={
                'Content-Type': "text/plain",
                'Content-Length': len(message),
            },
            body=message
        )
    elif request.path == '/user-agent':
        message = request.headers.get('User-Agent')
        response = Response(
            request.get_request_line(),
            HttpStatusCode.OK,
            headers={
                'Content-Type': "text/plain",
                'Content-Length': len(message),
            },
            body=message
        )
    else:
        response = Response(
            request.get_request_line(),
            HttpStatusCode.NOT_FOUND
        )

    conn.sendall(response.encode())
    conn.close()


def main():
    # Dev
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.bind((HOST, PORT))

    # Deploy
    server = socket.create_server(("localhost", 4221), reuse_port=True)
    server.listen()
    print("Server in port:", PORT)

    while True:
        conn, address = server.accept()
        print("Connected by:", address)
        thread = threading.Thread(
            target=client_handler,
            args=(conn,)
        )
        thread.start()


if __name__ == "__main__":
    main()