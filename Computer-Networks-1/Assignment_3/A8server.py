#TCP server program
import random,sys,time
from socket import *

clientIP = '127.0.0.1'
serverPort = 12345

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort))
print "Establishing Connection....."

seq = random.randint(1,1000)

flag = True
while flag:
    SYNPacket, clientAddr = serverSocket.recvfrom(2048)
    sap = SYNPacket.split(" ")
    print "Received "+SYNPacket
    if sap[1]=='S':
            flag = False
    else:
        print "Connection Failed"

SYNACKPacket = str(seq)+" "+str(int(sap[0])+1)+" SA"
serverSocket.sendto(SYNACKPacket, clientAddr)
seq = seq + 1 
temp=SYNACKPacket.split()
print "Sent SYNACK: Seq = "+temp[0]+" Ack = "+temp[1]+" TCP Flag = "+temp[2]
print "Connection Established"
h = int(sap[0])+1
window=window_temp={}
window[h]=""

while 1:
    message, clientAddr = serverSocket.recvfrom(2048)
    print "Received data: ", message
    respMsg = message.split(" ")
    if respMsg[2]=='F':
        l=window.keys()
        l.sort()
        for i in l:
            print "Last Packet "+str(window[i])+" sent to application layer"
            del window[i]
        finish=respMsg[1]+" "+str(int(respMsg[0])+1)+" F"
        serverSocket.sendto(finish, clientAddr) 
        print "Sent data: ", finish  
        finish=str(int(respMsg[1])+1)+" "+str(int(respMsg[0])+1)+" F"
        serverSocket.sendto(finish, clientAddr) 
        print "Sent data: ", finish
        message, clientAddr = serverSocket.recvfrom(2048)
        print "Received data: ", message
        respMsg = message.split(" ")
        if respMsg[1]=='F':
            serverSocket.close()
            print "Connection Closed"
            time.sleep(10)#Time Wait 
            sys.exit()
    if int(respMsg[0]) == h:
        del window[h]
        h=0
    
    window[int(respMsg[0])] = str(respMsg[3])

    l=window.keys()
    l.sort()    
    
    for i in l: #sorted(window.iteritems(), key=lambda (k,v): (v,k)):
        ack = i + len(window[i])    
        if (not window.has_key(i + len(window[i]))) or h!=0:#To make sure that we have received the very first packet
            break    
    

    l=window.keys()
    l.sort()
   
    
    for i in l:#sorted(window.iteritems(), key=lambda (k,v): (v,k)):
        if (window.has_key(i+len(window[i])) and h==0 ):
            print "Packet "+str(window[i])+" sent to application layer"
            del window[i] 
            break

    l=window.keys()
    l.sort()


    respMsg = str(seq)+" "+str(ack)+" A"
    respTemp= respMsg.split()
    x = random.randint(0,9)
    print "Ack Sent: Seq = "+respTemp[0]+" Ack = "+respTemp[1]+" TCP Flag = "+respTemp[2]
    if x<=7:
        serverSocket.sendto(respMsg, clientAddr)
        continue