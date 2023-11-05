"""A simple HTTP server."""
import argparse
from enum import Enum
import socket
import threading

HOST = "localhost"
PORT = 4221
BUFFER_ZISE = 1024
CRLF = '\r\n'
END_HEADERS = CRLF + CRLF
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"
BOLD = "\033[1m"


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


def logger(response: Response):
    if response.code.name == 'OK':
        message = f"{GREEN}"
    else:
        message = f"{RED}"
    message += f"{BOLD}{response.rq.method.name} "
    message += f"{response.rq.path}"
    message += RESET
    print(message)


def get_request(request, message, content_type="text/plain"):
    return Response(
        request.get_request_line(),
        HttpStatusCode.OK,
        headers={
            'Content-Type': content_type,
            'Content-Length': len(message),
        },
        body=message
    )


def get_request_not_found(request):
    return Response(
        request.get_request_line(),
        HttpStatusCode.NOT_FOUND
    )


def router(request: Request, directory: str = None):
    if request.path == '/':
        response = Response(request.get_request_line(), HttpStatusCode.OK)
    elif request.path.startswith('/echo/'):
        message = request.path.split('/echo/')[1]
        response = get_request(request, message)
    elif request.path == '/user-agent':
        message = request.headers.get('User-Agent')
        response = get_request(request, message)
    elif request.path.startswith('/files/') and directory:
        path = request.path.split('/files/')[1]
        try:
            with open(f"{directory}/{path}", 'r', encoding='UTF-8') as file:
                response = get_request(
                    request,
                    message=file.read(),
                    content_type="application/octet-stream")
        except FileNotFoundError:
            response = get_request_not_found(request)
    else:
        response = get_request_not_found(request)
    return response


def client_handler(conn, directory_path):
    data = conn.recv(BUFFER_ZISE)
    request = Request(data)
    response = router(request, directory_path)
    logger(response)
    conn.sendall(response.encode())
    conn.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", help="the directory path")
    args = parser.parse_args()
    directory_path = args.directory if args.directory else None
    # Dev
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.bind((HOST, PORT))

    # Deploy
    server = socket.create_server(("localhost", 4221), reuse_port=True)
    server.listen()
    print("Server in port:", PORT)

    while True:
        conn, _ = server.accept()
        thread = threading.Thread(
            target=client_handler, args=(conn, directory_path)
        )
        thread.start()


if __name__ == "__main__":
    main()