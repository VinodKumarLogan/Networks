#UDP server program
import sys, getopt
from socket import *

serverName = ''
serverPort = 12345

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print "UDP Server ready to receive data"
while 1:
    message, clientAddr = serverSocket.recvfrom(2048)
    print "Received data: ", message
    respMsg = message.upper()
    serverSocket.sendto(respMsg, clientAddr)
