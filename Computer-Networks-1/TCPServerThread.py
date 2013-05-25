#TCP server program
import sys, getopt
from socket import *
from threading import Thread

def handle_child(childSocket, childAddr):
    while True:
        message = childSocket.recv(2048)
        print "Received from ", childAddr, " data: ", message
        if len(message) == 0:
            childSocket.close()
            break;

        respMsg = message.upper()
        childSocket.send(respMsg)
    childSocket.close()
    print "Child thread completed\n"


serverName = ''
serverPort = 12346

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.listen(1); # change the value to higher number and study impact
print "TCP Server ready to receive data"
while 1:
    connSocket, clientAddr = serverSocket.accept()
    t= Thread(target=handle_child,
                args=(connSocket, clientAddr))
    t.start()