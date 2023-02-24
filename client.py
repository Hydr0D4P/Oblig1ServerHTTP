"""The webbrowser module is imported to open a local file in the default web browser.
The socket module is imported to establish a connection between the client and server.
The sys module is imported to access command-line arguments."""

import webbrowser
from socket import *
import sys

# The SERVER_ADDRESS, SERVER_PORT, FILENAME, and BUFFER_SIZE constants are initialized using the command-line arguments.
SERVER_ADDRESS = sys.argv[1]
SERVER_PORT = int(sys.argv[2])
FILENAME = sys.argv[3]
BUFFER_SIZE = 1024

"""
A client socket is created using the socket function from the socket module.
The socket is then connected to the server using its IP address and port number.
"""
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((SERVER_ADDRESS, SERVER_PORT))


"""
An HTTP GET request message is constructed. 
The message includes the filename, server address and port number,
and a connection close header to indicate that the client is done sending requests.
"""
request = 'GET /' + FILENAME + ' HTTP/1.1\r\n'
request += 'Host: ' + SERVER_ADDRESS + ':' + str(SERVER_PORT) + '\r\n'
request += 'Connection: close\r\n\r\n'

# Send the HTTP request message to the server, the encode method turns it into bytes
clientSocket.send(request.encode())


"""
The server's response message is received from the socket using the recv method.
The BUFFER_SIZE constant specifies the maximum amount of data that can be received at once.
The decode method is used to convert the received bytes into a string.
The response message is stored in the response variable.
"""

response = ''
while True:
    data = clientSocket.recv(BUFFER_SIZE).decode()
    if not data:
        break
    response += data


"""
The response message is split into a header and body using the \r\n\r\n separator.
The second parameter of the split method specifies the maximum number of splits to be made. 
Since the header and body are separated by only one \r\n\r\n, the maximum number of splits is set to one.
"""

header, body = response.split('\r\n\r\n', 1)


"""
If the header of the response message includes a 404 Not Found status code, then the message "404 Not Found" is printed.
Otherwise, the entire response message is printed to the console.

The response body is also written to a local file using the open function and the with statement. 
The file is opened in write mode and its contents are set to the body variable. 
Finally, the webbrowser.open function is used to open the local file in the default web browser.
"""

if 'HTTP/1.1 404 Not Found' in header:
    print('404 Not Found')
else:
    # Print the response
    print(response)

    """
    Dont know whether the following was required, but it basically stores the html file as a local file, 
    and runs it in the default web browser.
    """
    # Split the response message into header and body
    header, body = response.split('\r\n\r\n', 1)
    # Write the body to a local file and open it in a web browser
    with open(FILENAME, 'w') as file:
        file.write(body)
    webbrowser.open(FILENAME)

# Terminates the connection to free up system resources
clientSocket.close()