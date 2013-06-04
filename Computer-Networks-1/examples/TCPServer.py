#TCP server program
import sys, getopt
from socket import *

serverName = '127.0.0.1'
serverPort = 12345

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5) # change the value to higher number and study impact
print "TCP Server ready to receive data"
while 1:
    connSocket, clientAddr = serverSocket.accept()
    message = connSocket.recv(2048)
    print "Received data: ", message
    respMsg = message.upper()
    connSocket.send(respMsg)
    connSocket.close()
