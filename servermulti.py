from socket import *
import sys
import threading

def handle_client(serverSocket):
    serverSocket.listen(1)
    connectionSocket, addr = serverSocket.accept()
    try:
        print("Thread begin")
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

""" MAIN """

# Define constants for server address and port
SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 6789

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

    # Create a new socket on a new random available port for the client request
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.bind((SERVER_ADDRESS, 0)) # 0 to assign a random available port

    # Get the port number assigned to the client socket
    _, clientPort = clientSocket.getsockname()

    # Send the client the port number to use for the data connection
    connectionSocket.send(str(clientPort).encode())

    connectionSocket.close()
    # Start a new thread to handle the client request
    print(f"Generating new thread on port {clientPort} for user {connectionSocket}")
    t = threading.Thread(target=handle_client, args=(clientSocket,))
    t.start()