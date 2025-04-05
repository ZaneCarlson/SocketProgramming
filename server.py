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


    while True:
        data = socket_client.recv(1024).decode()
        print(f"Received request: {data.strip()}")
        if data == "MSGGET\n":
            sending_msg = "200 OK\n" + message
            socket_client.sendall(sending_msg.encode())
            continue
        if data == "MSGSTORE\n":
            sending_msg = "200 OK"
            socket_client.sendall(sending_msg.encode())
            data = socket_client.recv(1024).decode()
            if data != "QUIT\n" and data != "SHUTDOWN\n":
                print(f"Received message: {data.strip()}")
                message = data.strip()
                sending_msg = "200 OK"
                socket_client.sendall(sending_msg.encode())
                continue
            continue
        if data == "QUIT\n":
            sending_msg = "200 OK"
            socket_client.sendall(sending_msg.encode())
            print("Client has disconnected.")
            break
        if data == "SHUTDOWN\n":
            sending_msg = "300 PASSWORD REQUIRED"
            socket_client.sendall(sending_msg.encode())
            password_attempt = socket_client.recv(1024).decode()
            print(f"Received password attempt: {password_attempt.strip()}")
            if password != password_attempt.strip():
                print("Invalid password received.")
                sending_msg = "400 INVALID PASSWORD"
                socket_client.sendall(sending_msg.encode())
                continue
            sending_msg = "200 OK SHUTTING DOWN"
            socket_client.sendall(sending_msg.encode())
            socket_server.close()
            break
        else:
            break

    if data == "SHUTDOWN\n":
        print("Server is shutting down.")  
        break