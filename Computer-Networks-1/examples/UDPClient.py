#UDP client program
import sys, getopt
from socket import *

serverName = '127.0.0.1'
serverPort = 12345

clientSocket = socket(AF_INET, SOCK_DGRAM)
message = raw_input('Input in lower case sentence:\n')
clientSocket.sendto(message, (serverName, serverPort))
recdMessage, serverAddress = clientSocket.recvfrom(2048)
print recdMessage
clientSocket.close()
