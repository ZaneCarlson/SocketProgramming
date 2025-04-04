import socket

HOST = '127.0.0.1'
SERVER_PORT = 6789
password = "123!abc"
message = "An apple a day keeps the doctor away."

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_server.bind((HOST, SERVER_PORT))
socket_server.listen(1)
print(f"Server is listening on {HOST}:{SERVER_PORT}")

while True:
    socket_client, client_address = socket_server.accept()
    print(f"Connection from {client_address} has been established.")
    socket_client.sendall(message.encode())

    data = socket_client.recv(1024).decode()
    if data == "MSGGET\n":
        msg = "200 OK\n" + message
        socket_client.sendall(msg.encode())

    socket_client.close()