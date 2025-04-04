import socket

HOST = '127.0.0.1'
SERVER_PORT = 6789

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((HOST, SERVER_PORT))

while True:

    request = input("Enter your request (MSGGET, MSGSTORE, QUIT, or SHUTDOWN): ")
    if request == "QUIT":
        socket_client.sendall(request.encode())
        while True:
            msg = socket_client.recv(1024).decode()
            if msg == "200 OK":
                print(msg)
                break
        break
    
    request += "\n"

    #if request == "SHUTDOWN\n":
        
    #    print("Server is shutting down.")
    #    socket_client.sendall(request.encode())
    #    break

    if request == "MSGGET\n":
        socket_client.sendall(request.encode())
        while True:
            msg = socket_client.recv(1024).decode()
            if msg == "200 OK":
                print(msg)
                break

    #elif request == "MSGSTORE\n":
    #    msg = input("enter your message to store:")
    #    socket_client.sendall(msg.encode())

    else:
        print("Invalid request. Please try again.")
        continue


socket_client.close()
print("Connection closed.")