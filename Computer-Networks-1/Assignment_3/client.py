from socket import *
import random,time,argparse,sys


parser = argparse.ArgumentParser()
parser.add_argument("-N","--packets", help="Enter the total numnber of packets to be sent(minimum 20). Default value is 20 ",default=20,type=int)
parser.add_argument("-t","--timeout", help="Enter the timeout value in seconds. Default value is 2s ",default=2,type=int)
parser.add_argument("-s","--serverip", help="Enter the server's IP address. Default value is 127.0.0.1",default="127.0.0.1")
parser.add_argument("-p","--serverport", help="Enter the server's port number. Default value is 12345",default=12345)
parser.add_argument("-w","--windowsize", help="Enter the congestion window's size. Default value is 4",default=4,type=int)
parser.add_argument("-l","--packetloss", help="Enter the average packet loss as percentage.Default value is 30%",default=30,type=int)
args = parser.parse_args()


serverIP = args.serverip
serverPort = args.serverport
def_cwnd = cwnd = args.windowsize
dtimeout = args.timeout
packets = args.packets
ploss=args.packetloss
init_time = time.time()
psent = 0 #Holds the number of packets sent
seq = random.randrange(1,1000) #Holds the sequence number 
ack = 100   #Holds the acknowledgement number
clientSocket = socket(AF_INET, SOCK_DGRAM) #Creating the UDP socket   
p2bsent = 0 #Holds the number of packets sent in each burst
window = {} #Window to hold the packet data

print "Establishing Connection....."
SYNpacket = str(seq)+" S"


print "Sent "+SYNpacket
flag = True
c = 0
clientSocket.sendto(SYNpacket, (serverIP, serverPort))
clientSocket.settimeout(dtimeout)
try:
    SYNACKPacket, serverAddress = clientSocket.recvfrom(2048)
except timeout: c=1
if c==1:
    print "Connection Failed"
    sys.exit(0)        
   
sap = SYNACKPacket.split(" ")
print "Received "+SYNACKPacket 
if sap[2]=="SA":
    print "Connection Established"
else:
    print "Connection Failed"
    sys.exit(0)

seq = int(sap[1])
ack = int(sap[0])+1
m = 'A'

while psent<packets:
    p2bsent = 0
    sendBase = 0 
    
    #Sending the Packets 
    while p2bsent<cwnd and (psent+p2bsent)<packets:
        message = ""        
        r = random.randrange(1,100)
        for i in range(r):
            message = message + m
        m = chr(ord(m)+1)
        window[seq] = message #Adding the packet data to the window before it is transmitted to the server
        message = str(seq)+" "+str(ack)+" A "+str(message) #Creating the message
        if p2bsent==sendBase: #Checking if its the first packet
                T1 = time.time() #starting the timer
                clientSocket.settimeout(dtimeout) #setting the socket timeout
                sendBase = seq
        q = random.randrange(0,10)
        seq = seq + len(window[seq]) #Incrementing the sequence number
        p2bsent = p2bsent + 1 #Updating the number of packets sent in the current burst
        loss=int((100-ploss)/10)
        temp = message.split(" ")
        curr_time = time.time() - init_time
        print "Sent Packet (Original) at "+str(curr_time)[:6]+"s Seq = "+temp[0]+" Ack = "+temp[1]+" Data = "+temp[3]
        if q<=loss:
            clientSocket.sendto(message, (serverIP, serverPort)) #Sending the message
        else:
            continue                


    
    T2 = time.time()  #
    f = 0 #flag to handle retransmission
    ca = 0 #Counter to check whether congestion has occured or not
    
    #Waiting for Acks
    while int(T2-T1)<=dtimeout: #Receive Acks till timeout occurs
        T2=time.time()   

        try:
            recd, serverAddress = clientSocket.recvfrom(2048) #Receive the Ack if possible
        except timeout: f = 1 #If there is a timeout set the flag f to 1 (for retransmission)
        if f==0: #An Ack has been received 
            recdMessage = recd.split(" ")
            y = int(recdMessage[1])
            curr_time = time.time() - init_time
            print "Ack received at "+str(curr_time)[:6]+"s  : Seq = "+recdMessage[0]+" Ack = "+str(y)+" TCP Flag = "+recdMessage[2] #Displaying the Ack
            if y>=sendBase: #checking if the all the packets till the Ack's value are delivered to the server or not
                temp = sendBase
                sendBase = y #Packet with seq no sendBase have been delivered tp the server
                
                l=window.keys()
                l.sort()
                j=0
                for i in l:
                    #Removing the packets in window which have been delivered (shifting the window)
                    if (i+len(window[i]))<=y: #If there is a key in the window whose value is equal to the Ack
                        del window[i] #deleting window entry
                        j = j + 1
                if j==1:
                    ca = ca + 1 
                if not window:
                    break
                if window: #If there are packets in the window which are yet to be Acked
                    T1 = time.time()  
                    T2 = time.time()
                    clientSocket.settimeout(dtimeout) #Resetting timeout
        
        else:
            if window: #If there are more Acks to be received
                
                l=window.keys()
                l.sort()
                for i in l:
                    clientSocket.settimeout(dtimeout) #Resetting timeout
                    message = str(i)+" "+str(ack)+" A "+str(window[i])
                    loss=int((100-ploss)/10)
                    q=random.randrange(0,9)
                    temp = message.split(" ")
                    curr_time = time.time() - init_time
                    ca=0
                    print "Sent Packet (Retransmitted) at "+str(curr_time)[:6]+"s Seq = "+temp[0]+" Ack = "+temp[1]+" Data = "+temp[3]
                    if q<=loss:
                        clientSocket.sendto(message, (serverIP, serverPort)) #Sending the message
                    T1 = time.time()
                    T2 = time.time()
                f = 0 #Resetting the flag to no retransmission
        
    psent = psent + p2bsent
    if ca == cwnd:#No congestion
        cwnd = cwnd + 1
        print "Congestion Window =",cwnd
    else:#Congestion Avoidance
        cwnd = def_cwnd
        print "Congestion Window =",cwnd
message= recdMessage[1]+" "+str(int(recdMessage[0])+1)+" F"
clientSocket.sendto(message, (serverIP, serverPort))
print "Sent "+message
recd, serverAddress = clientSocket.recvfrom(2048)
print "Received "+recd
recdMessage = recd.split(" ")
if recdMessage[2]=='F':
            recd, serverAddress = clientSocket.recvfrom(2048)
            print "Received "+recd
            recdMessage = recd.split(" ")
            message= recdMessage[1]+" F"
            clientSocket.sendto(message, (serverIP, serverPort))
            print "Sent "+message
            print "Connection Closed"
            time.sleep(10)#Time Wait       
            clientSocket.close()