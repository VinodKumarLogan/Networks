#TCP client program
import sys
from socket import *

serverName = '127.0.0.1'
serverPort = 12345

# create a socket and connect to server
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))


# get the data from user via stdin
message = raw_input('Input in lower case sentence:\n')
clientSocket.send(message)
recdMessage = clientSocket.recv(2048)
print "Received from server: ", recdMessage
clientSocket.close()
