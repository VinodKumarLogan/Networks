# importing the required classes
from socket import *
import random,time,sys
import argparse 

# parsing the arguments
parser = argparse.ArgumentParser()
parser.add_argument("-N","--packets", help="Enter the total numnber of packets to be sent(minimum 20). Default value is 20 ",default=20,type=int)
parser.add_argument("-t","--timeout", help="Enter the timeout value in seconds. Default value is 2s ",default=2,type=int)
parser.add_argument("-s","--serverip", help="Enter the server's IP address. Default value is 127.0.0.1",default="127.0.0.1")
parser.add_argument("-p","--serverport", help="Enter the server's port number. Default value is 12345",default=12345,type=int)
parser.add_argument("-w","--windowsize", help="Enter the congestion window's size. Default value is 4",default=4,type=int)
parser.add_argument("-l","--packetloss", help="Enter the average packet loss as percentage.Default value is 30",default=30,type=int)

args = parser.parse_args()

serverIP = args.serverip # Stores the server IP
serverPort = args.serverport # Stores the server Port number
def_cwnd = cwnd = args.windowsize # Stores the default congestion window size
dtimeout = args.timeout # Stores the timeout value in seconds
packets = args.packets # Stores the number of packets to be sent to the server in this session
ploss=args.packetloss # Stores the packet loss value in percentage

init_time = time.time()
psent = 0 # Holds the number of packets sent
seq = random.randrange(1,1000) # Generating a random sequence number and storing it 
ack = 100   # Holds the acknowledgement number
clientSocket = socket(AF_INET, SOCK_DGRAM) # Creating the UDP socket   
p2bsent = 0 # Holds the number of packets sent in each burst
window = {} # Window(python dictionary) to hold the packet data

print "Establishing Connection....."
SYNpacket = str(seq)+" S" # Creating the SYN packet with the TCP flags and initial sequence number


print "Sent "+SYNpacket # Displaying the SYN packet which is due to be sent
c = 0 # A flag to handle timeout senario

clientSocket.sendto(SYNpacket, (serverIP, serverPort)) # Sending the SYN packet
clientSocket.settimeout(dtimeout) # Setting the timeout
try:
    SYNACKPacket, serverAddress = clientSocket.recvfrom(2048) # Receiving the SYNACK packet frrom the server
except timeout: c=1 # Exception handledwhen the timeout occurs
if c==1: # If the timeout has occurred
    print "Connection Failed"
    clientSocket.close()
    sys.exit(0) # Exiting after closing the connection * we haven't handled retransmission of SYN packet      
   
sap = SYNACKPacket.split(" ") # Spliting the SYNACK packet's contents into chunks for further processing *we are using space as delimiter for packet contents
print "Received "+SYNACKPacket 
if sap[2]=="SA": # If there is TCP flag named SA in the contents then the connection is established else close and exit
    print "Connection Established"
else:
    print "Connection Failed"
    clientSocket.close()
    sys.exit(0)

seq = int(sap[1]) # Updating the sequence number after the 3 way handshake
ack = int(sap[0])+1 # Updating the ack number after the 3 way handshake
m = 'A' # Setting the default value for the data field

while psent<packets: # This loop will run until all the packets are succesfully acked
    p2bsent = 0 # Stores the number of packets to be sent in the current burst
    sendBase = 0  # Stores the seq number of the packet which has been acked recently
    
    #Sending the Packets  
    while p2bsent<cwnd and (psent+p2bsent)<packets: # This lop will run until the all the packets in the congestion window are sent 
        message = "" # Empty message to store the packet data        
        r = random.randrange(1,100) # Generating a random number to have that many bytes of data in the packet excluding SYn and ACK
        for i in range(r):
            message = message + m # Creating the Data
        m = chr(ord(m)+1) # Incrementing the message to the next character
        window[seq] = message #Adding the packet data to the window before it is transmitted to the server
        message = str(seq)+" "+str(ack)+" A "+str(message) #Creating the packet
        if p2bsent==sendBase: #Checking if its the first packet
                T1 = time.time() #starting the timer
                clientSocket.settimeout(dtimeout) #setting the socket timeout
                sendBase = seq # setting the sendBase to the first seq number in the current burst of packets
        q = random.randrange(0,10) # random number to simulate packet loss
        seq = seq + len(window[seq]) #Incrementing the sequence number
        p2bsent = p2bsent + 1 #Updating the number of packets sent in the current burst
        loss=int((100-ploss)/10) # Calculating the packet loss percentage
        temp = message.split(" ") # Spliting the contents of the packet and displaying it to the user
        curr_time = time.time() - init_time # Calculating the time at whic the packet is sent with respect to the inititial time
        print "Sent Packet (Original) at "+str(curr_time)[:6]+"s Seq = "+temp[0]+" Ack = "+temp[1]+" Data = "+temp[3]
        if q<=loss:
            clientSocket.sendto(message, (serverIP, serverPort)) #Sending the message
        else:
            continue # Packet Loss scenario               


    
    T2 = time.time()  # To handle timeout explicitly along with settimeout()
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
                
                #Sorting the window contents
                l=window.keys() # List to store the keys of the window which is to be sorted
                l.sort()
                j=0 # counter to keep track of the number of entries deleted in the window when the ack is received
                for i in l:
                    #Removing the packets in window which have been delivered (shifting the window)
                    if (i+len(window[i]))<=y: #If there is a key in the window whose value is equal to the Ack
                        del window[i] #deleting window entry
                        j = j + 1
                if j==1: # If the number of packets deleted from the window is 1 , it means that ack for that packet has been received and hence its not a cumulative ack that is handled
                    ca = ca + 1 # Incrementing the counter to keep track of the number of ack received
                if not window: # If the window is empty , it means that all the packets have been successfully acked within the timeout
                    break
                if window: #If there are packets in the window which are yet to be Acked
                    T1 = time.time()  
                    T2 = time.time()
                    clientSocket.settimeout(dtimeout) #Resetting timeout
        
        else:
            if window: #If there are more Acks to be received
                
                #Sorting the window
                l=window.keys()
                l.sort()
                for i in l: # Retransmitting the unacked packets present in the window
                    clientSocket.settimeout(dtimeout) #Resetting timeout so that all the unacked packets can be retransmitted
                    message = str(i)+" "+str(ack)+" A "+str(window[i]) # creating the packet which is to be retransmitted 
                    loss=int((100-ploss)/10) # Calculating the packet loss percent
                    q=random.randrange(0,9) # Generating a randow value to simlulate packet loss
                    temp = message.split(" ") # Splitting the message to display the packet contents to the user
                    curr_time = time.time() - init_time # Calculating the time at which the packet is sent
                    ca = 0 # the congestion counter is set to 0 because there is congestion in the network hence the acknowledgements received henceforth should not be taken into account
                    print "Sent Packet (Retransmitted) at "+str(curr_time)[:6]+"s Seq = "+temp[0]+" Ack = "+temp[1]+" Data = "+temp[3]
                    if q<=loss: # Simulating packet loss
                        clientSocket.sendto(message, (serverIP, serverPort)) #Sending the message
                    T1 = time.time()
                    T2 = time.time()
                f = 0 #Resetting the flag to no retransmission
        
    psent = psent + p2bsent # Incrementing the value of psent to psent + p2bsent indicating that p2bsent number of packets have been sent
    #Congestion Avoidance simulation
    if ca == cwnd:#No congestion in the network because number of packets sent is equal to the number of acks received ,so, the congestion window size will be incremented by 1
        cwnd = cwnd + 1 
    else: # the congestion window size is reset to its default value because the number of packets sent is not equal to the number of acks received which means that there is some congestion in the network
        cwnd = def_cwnd   
    print "Congestion Window = ",cwnd #Displaying the congestion window size
message= recdMessage[1]+" "+str(int(recdMessage[0])+1)+" F" # Creating the FIN packet 
clientSocket.sendto(message, (serverIP, serverPort)) # Sending the FIN packet to the server
print "Sent "+message
recd, serverAddress = clientSocket.recvfrom(2048) # Receiving the acknowledgement of the FIN packet from the server 
print "Received "+recd
recdMessage = recd.split(" ") # Parsing the received ack and checking whether the flags are correct or not
if recdMessage[2]=='F':
            recd, serverAddress = clientSocket.recvfrom(2048) # Receiving the FIN segment from the server
            print "Received "+recd
            recdMessage = recd.split(" ")
            message= recdMessage[1]+" F" # Creating the acknowledgement packet
            clientSocket.sendto(message, (serverIP, serverPort)) # Sending the acknowledgement to the server
            print "Sent "+message
            print "Connection Closed" 
            time.sleep(10)#Time Wait       
            clientSocket.close() # Closing the connection
