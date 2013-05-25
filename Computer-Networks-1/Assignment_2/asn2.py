#asn2.py

#importing socket for establishing connection with mailserver 
#importing sys to deal with command line arguements
#importing argparse to parse and manipulate command line arguements
#import string to split the recipient's mail IDs

from socket import *
from sys import *
import argparse 
from string import *

def usage():
    print "python asn2.py -s <servername> -p <port_number> -n <hostname> -m <mailID_of_the_sender> -r <mailID_of_the_recipients>"
    sys.exit(0)

# Adding options
parser = argparse.ArgumentParser()
parser.add_argument("-s","--servername", help="enter the server name. Default value is 127.0.0.1 ",default="127.0.0.1")
parser.add_argument("-p","--portno", help="enter the port number. Default value is 25 ",default=25,type=int)
parser.add_argument("-n","--hostname", help="enter the host name. Default value is localhost ",default="localhost")
parser.add_argument("-m","--mailfrom", help="enter the sender's email id",default="")
parser.add_argument("-r","--mailto", help="enter the recipient's email id(s). Separated by ',' if there are more than one recipients",default="")
#parsing the arguements
args = parser.parse_args()
mailserver =  args.servername # holds the server name
serverPort =  args.portno # holds the server port
hostname =  args.hostname # holds the hostname
mailFrom =  args.mailfrom # holds the mail ID of the sender
rcpt = args.mailto # holds the recipient's ID

flagm = 0
flagr = 0
# If the there is no arguement given for mail from
if mailFrom=="":
	flagm=1

# If the there is no arguement given for mail from
if rcpt == "":
	flagr=1

# Creating socket called clientSocket and establishing a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverPort)) # Establishing connection to the server
recv = clientSocket.recv(1024) # Storing the server's response
print recv # displaying server response
if recv[:3] != '220': # checking for request failure
    print '220 reply not received from server.'
    usage()

# Sending HELO command and printing server response.
heloCommand = 'EHLO '+hostname+'\r\n'
print heloCommand
clientSocket.send(heloCommand) # sending ehlo command to the server (request)
recv1 = clientSocket.recv(1024) # Storing the server's response
print recv1 # displaying server response

if recv1[:3] != '250': # checking for request failure
    print '250 reply not received from server.'
    usage()

check ='y'

while check == 'y':

    # Sending MAIL FROM command and printing server response.
    # If the user has left the mail from parameter empty
    if flagm==1:
        mailFrom = raw_input("Enter the sender's email ID : ") # Accepting sender's mail ID
    mailFromCommand = 'MAIL FROM: '+mailFrom+' \r\n'
    print mailFromCommand
    clientSocket.send(mailFromCommand) # sending the MAIL FROM request to the server
    recv2 = clientSocket.recv(1024) # Storing the server's response
    print recv2 # displaying server response
    if recv2[:3] != '250': # checking for request failure
        print '250 reply not received from server.'
        usage()

    # Sending RCPT TO command and printing server response.
    # If the user has left the rcpt to parameter empty
    if flagr==1:
	rcpt = raw_input("Enter the Recipient's mail ID(s) :  ") # Accepting sender's mail ID
    recipients = split(rcpt,",") # If the user had entered multiple IDs with , separating them 
    for recipient in recipients:
        rcptToCommand = 'RCPT TO: '+recipient+'\r\n'
        print rcptToCommand
        clientSocket.send(rcptToCommand) # sending the RCPT TO request to the server for each recipient
        recv3 = clientSocket.recv(1024) # Storing the server's response
        print recv3 # displaying server response
        if recv3[:3] != '250': # checking for request failure
            print '250 reply not received from server.'
            usage()

    # Sending DATA command and printing server response.
    dataCommand = 'DATA\r\n'
    print "DATA\n(Enter the content of the mail)"
    clientSocket.send(dataCommand) # sending the DATA request to the server
    recv4 = clientSocket.recv(1024) # Storing the server's response
    print recv4 # displaying server response
    if recv4[:3] != '354': # checking for request failure
        print '354 reply not received from server.data'
        usage()

    # Sending message data.
    
    #Accepting multiline input with '.' as the terminating character
    flag=1
    y=""
    while flag==1:
        x=raw_input()
        y+=x+'\n'
        if x[:1] is '.':
            flag=0
    mailContent = y[:(len(y)-2)]
    #mailContent = raw_input()
    q = 0
    mailContent = '\r\n'+mailContent+'\r\n'
    clientSocket.send(mailContent) # sending the mail content to the server


    # Message ends with a single period.
    endCommand = '\r\n.\r\n'
    clientSocket.send(endCommand) # terminating the DATA request
    recv5 = clientSocket.recv(1024) # Storing the server's response
    print recv5 # displaying server response
    
    flagm=1
    flagr=1
    #If the user wants to send more emails 
    check = raw_input("Do you want to send another mail using the same connection ? (y/n) : ")
    

# Sending QUIT command if the user decides to stop mailing on the same connection
quitCommand = 'QUIT\r\n'
print quitCommand
clientSocket.send(quitCommand)
recv6 = clientSocket.recv(1024) # Storing the server's response
print recv6 # displaying server response 
if recv6[:3] != '221': # checking for request failure
    print '221 reply not received from server.quit'
    usage()
