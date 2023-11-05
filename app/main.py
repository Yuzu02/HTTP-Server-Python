import socket

CRLF = "\r\n"
HEADERS_END = CRLF + CRLF
HTTP_200 = "HTTP/1.1 200 OK" + HEADERS_END
BUFFER = 1024

def main():
    print("Logs from your program will appear here!")
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    client_socket, client_address = server_socket.accept()

    with client_socket:
        data = client_socket.recv(BUFFER)
        client_socket.send(HTTP_200.encode())

if __name__ == "__main__":
    main()
