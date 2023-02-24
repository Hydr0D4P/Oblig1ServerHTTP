from socket import *
import sys
import threading

# Define constants for server address and port
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 6789

def handle_client(connectionSocket):
    try:
        # Receive the client's request message
        message = connectionSocket.recv(1024).decode()

        # Extract the filename from the request message
        filename = message.split()[1][1:]

        # Open the file and read its contents
        with open(filename, 'rb') as file:
            outputdata = file.read()

        # Send an HTTP response header
        response = 'HTTP/1.1 200 OK\r\n'
        response += 'Content-Type: text/html; charset=UTF-8\r\n'
        response += 'Content-Length: ' + str(len(outputdata)) + '\r\n\r\n'
        connectionSocket.send(response.encode())

        # Send the requested file to the client
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i:i+1])
        print(f"{filename} sent to user {connectionSocket}, connection closing")
        # Close the connection socket
        connectionSocket.close()

    except IOError:
        # If the file is not found, send a 404 response message
        response = 'HTTP/1.1 404 Not Found\r\n'
        response += 'Content-Type: text/html; charset=UTF-8\r\n\r\n'
        response += '<html><body><h1>404 Not Found</h1></body></html>'
        connectionSocket.send(response.encode())

        # Close the connection socket
        connectionSocket.close()

# Create a server socket
serverSocket = socket(AF_INET, SOCK_STREAM)

# Bind the socket to a specific address and port
serverSocket.bind((SERVER_ADDRESS, SERVER_PORT))

# Listen for incoming connections
serverSocket.listen(5)
print('The server is ready to receive...')

while True:
    # Wait for a connection request
    connectionSocket, addr = serverSocket.accept()

    # Create a new thread to handle the client request
    t = threading.Thread(target=handle_client, args=(connectionSocket,))
    t.start()