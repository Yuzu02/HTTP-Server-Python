import socket

HOST, PORT = "localhost", 4221

code_status = {
    200: 'OK',
    404: 'Not Found',
}


def parsed_response(code: int, headers: dict = {}, body: str = "") -> str:
    response_headers = f"HTTP/1.1 {code} {code_status.get(code)}\r\n"
    for key in headers:
        response_headers += f"{key}: {headers[key]}\r\n"
    response_headers += "\r\n"
    return response_headers + body


def main():
    # Dev
    # server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server.bind((HOST, PORT))
    # server.listen(5)

    # Deploy
    server = socket.create_server(("localhost", 4221), reuse_port=True)

    print("Server in port:", PORT)
    conn, address = server.accept()
    print("Connected by:", address)

    data = conn.recv(1024).decode().splitlines()
    print(data[0])

    http_status = data[0].split(' ')
    path = http_status[1]
    if http_status[1] == '/':
        response = parsed_response(200)
    elif path.startswith('/echo/'):
        message = path.split('/echo/')[1]
        response = parsed_response(200, {
            "Content-Type":  "text/plain",
            "Content-Length": f"{len(message)}"
        }, f"{message}")
    else:
        response = parsed_response(404)
    conn.sendall(response.encode())


if __name__ == "__main__":
    main()