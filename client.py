import socket
import sys

if len(sys.argv) != 2:
    print("Usage: python client.py <server_ip_address>")
    sys.exit(1)

serverIP = sys.argv[1]
SERVER_PORT = 6789

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((serverIP, SERVER_PORT))

while True:

    request = input("Enter your request (MSGGET, MSGSTORE, QUIT, or SHUTDOWN): \nc: ")
    request += "\n"

    if request == "MSGSTORE\n":
            socket_client.sendall(request.encode())
            recieved_msg = socket_client.recv(1024).decode()
            print("s:" + recieved_msg)
            sending_msg = input("c:")
            if sending_msg != "QUIT" and sending_msg != "SHUTDOWN":
                socket_client.sendall(sending_msg.encode())
                recieved_msg = socket_client.recv(1024).decode()
                print("s:" + recieved_msg)
                continue
            else: 
                request = sending_msg + "\n"
                socket_client.sendall(request.encode())
            
    
    if request == "QUIT\n":
        socket_client.sendall(request.encode())
        print(request)
        msg = socket_client.recv(1024).decode()
        if msg == "200 OK":
            print("s:" + msg)
        break

    if request == "SHUTDOWN\n":
       socket_client.sendall(request.encode())
       recieved_msg = socket_client.recv(1024).decode()
       print("s:" + recieved_msg)
       sending_msg = input("c:")
       socket_client.sendall(sending_msg.encode())
       recieved_msg = socket_client.recv(1024).decode()
       if recieved_msg == "200 OK SHUTTING DOWN":
            print("s:" + recieved_msg)
            break
       elif recieved_msg == "400 INVALID PASSWORD":
            print("s:" + recieved_msg)
            continue

    if request == "MSGGET\n":
        socket_client.sendall(request.encode())
        recieved_msg = socket_client.recv(1024).decode()
        print("s:" + recieved_msg)
        continue

    


    else:
        print("Invalid Command, try again.")
        continue


socket_client.close()
print("Connection closed.")