#import socket module
from socket import *
import time
serverSocket = socket(AF_INET, SOCK_STREAM)
#Prepare a sever socket


httpserver = "127.0.0.1"
serverPort = 80
#Fill in start
serverSocket.connect((httpserver, serverPort)) # Establishing connection to the server
recv = serverSocket.recv(1024) # Storing the server's response
print recv # displaying server response
#Fill in end
x=True
while x:
    #Establish the connection
    print 'Ready to serve...'
    connectionSocket, addr = 80,"127.0.0.1"
    #Fill in start    
    #Fill in end
    try:
        message =  "http://127.0.0.1:80/sample.html"  
	#Fill in start	
        #Fill in end
        filename = message.split("/")
        filename = filename[-1:]
        for x in filename:
              print x
        filename = x
        print filename
        f = open("/var/www/"+filename,"r")
        outputdata = f.read()
        print outputdata
        x=False
        localtime = str(time.asctime( time.localtime(time.time())))
        outputdata = "HTTP/1.1 200 OK\nDate:"+localtime+""
        #Fill in start	
        #Fill in end
        #Send one HTTP header line into socket
        #Fill in start
        #Fill in end
        #Send the content of the requested file to the client
        #for i in range(0, len(outputdata)):
        #    connectionSocket.send(outputdata[i])
        #connectionSocket.close()
    except IOError:
        #Send response message for file not found
        #Fill in start
        #Fill in end
        #Close client socket
        #Fill in start
        #Fill in end
                   serverSocket.close()
    x=False                
