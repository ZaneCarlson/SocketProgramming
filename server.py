import socket

HOST = '127.0.0.1'
SERVER_PORT = 6789
password = "123!abc"                              # Password for shutdown command
message = "An apple a day keeps the doctor away." # Default Message of the day

socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # Create a TCP socket
socket_server.bind((HOST, SERVER_PORT))                             # Bind the socket to the host and port
socket_server.listen(1)
print(f"Server is listening on {HOST}:{SERVER_PORT}")

while True: #loop while waiting for a connection
    socket_client, client_address = socket_server.accept() # Accept a connection from a client
    print(f"Connection from {client_address} has been established.")


    while True: #loop through the clients commands
        data = socket_client.recv(1024).decode() # Receive data from the client
        print(f"Received request: {data.strip()}")
        if data == "MSGGET\n":
            sending_msg = "200 OK\n" + message
            socket_client.sendall(sending_msg.encode())
            continue
            #if the client requests the message of the day then send it to them and continue the loop

        elif data == "MSGSTORE\n":
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
            #if the client reqests to store a message then prompt them for a message and store it in the variable message and cofirm that it was stored. continue command loop.
            #if the client sends QUIT or SHUTDOWN then continue the loop and wait for the next command (client side will automatically send a repeat command of QUIT or SHUTDOWN).

        elif data == "QUIT\n":
            sending_msg = "200 OK"
            socket_client.sendall(sending_msg.encode())
            print("Client has disconnected.")
            break
            #if the client requests to quit then send them a 200 OK message and break out of the command loop.

        elif data == "SHUTDOWN\n":
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
            #if the client requests to shutdown then send them a "password required" message and wait for them to send the password. if the password is correct then send them a 200 OK SHUTTING DOWN message and close the server and break.
        else:
            break

    if data == "SHUTDOWN\n":
        print("Server is shutting down.")  
        break
        #Shutdown command breaks out of the main loop, and breaks out of the connection loop. 