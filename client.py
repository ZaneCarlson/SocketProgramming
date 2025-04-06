import socket
import sys

if len(sys.argv) != 2: # Check if the correct number of arguments is provided
    print("Usage: python client.py <server_ip_address>") #display the correct usage of the program
    sys.exit(1)

serverIP = sys.argv[1] # Get the server IP address from the command line argument
SERVER_PORT = 6789

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect((serverIP, SERVER_PORT))
# Create a TCP socket and connect to the server

while True: # Loop through the clients commands

    request = input("Enter your request (MSGGET, MSGSTORE, QUIT, or SHUTDOWN): \nc: ")
    request += "\n"
    # Take the user input and append a newline character to it

    if request == "MSGSTORE\n":
        socket_client.sendall(request.encode())
        recieved_msg = socket_client.recv(1024).decode()
        print("s:" + recieved_msg)
        sending_msg = input("c:")
        socket_client.sendall(sending_msg.encode())
        recieved_msg = socket_client.recv(1024).decode()
        print("s:" + recieved_msg)
        continue
        # If the client requests to MSGSTORE then send the message and wait for a 200 OK. 
        # Then prompt the user for a message to store and send it to the server.
        # Wait for a 200 OK message and print it to the console. Then continue the loop.
    
    elif request == "QUIT\n":
        socket_client.sendall(request.encode())
        msg = socket_client.recv(1024).decode()
        if msg == "200 OK":
            print("s:" + msg)
        break
        # If the client requests QUIT then send the request to the server and wait for 200 OK then break the loop so the connection will be closed.
        

    elif request == "SHUTDOWN\n":
       socket_client.sendall(request.encode())
       recieved_msg = socket_client.recv(1024).decode()
       print("s:" + recieved_msg)
       sending_msg = input("c:")
       socket_client.sendall(sending_msg.encode())
       recieved_msg = socket_client.recv(1024).decode()
       if recieved_msg == "200 OK SHUTTING DOWN":
            break
       elif recieved_msg == "400 INVALID PASSWORD":
            print("s:" + recieved_msg)
            continue
        # If the client requests SHUTDOWN then send the request to the server and wait for a 300 PASSWORD REQUIRED message.
        # Then prompt the user for a password and send it to the server.
        # Wait for a 200 OK SHUTTING DOWN message and break the loop to close the connection.
        # If the password is invalid then print the message and continue the loop.

    elif request == "MSGGET\n":
        socket_client.sendall(request.encode())
        recieved_msg = socket_client.recv(1024).decode()
        print("s:" + recieved_msg)
        continue
        # If the client requests MSGGET then send that request. then recieve the message of the day and print it to the console.
        # Then continue the loop.

    else:
        print("Invalid request. Please try again.")
        continue
        # If the request is invalid then print an error message and continue the loop.


socket_client.close()
print("Connection closed.")
# make sure the connection is closed and end the program.