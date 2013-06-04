#smtp_client_skel.py

from socket import *
from sys import *
import argparse 
from string import *

parser = argparse.ArgumentParser()
parser.add_argument("-s","--servername", help="enter the server name. Default value is 127.0.0.1 ",default="127.0.0.1")
parser.add_argument("-p","--portno", help="enter the port number. Default value is 25 ",default=25,type=int)
parser.add_argument("-n","--hostname", help="enter the host name. Default value is localhost ",default="localhost")
parser.add_argument("-m","--mailfrom", help="enter the sender's email id",default="")
parser.add_argument("-r","--mailto", help="enter the recipient's email id(s). Separated by ',' if there are more than one recipients",default="")
args = parser.parse_args()
mailserver =  args.servername
serverPort =  args.portno
hostname =  args.hostname
mailFrom =  args.mailfrom
rcpt = args.mailto
flagm = 0
flagr = 0
if mailFrom=="":
	flagm=1
if rcpt == "":
	flagr=1

# Choosing localhost as the default mail server



# Creating socket called clientSocket and establishing a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((mailserver, serverPort))
recv = clientSocket.recv(1024)
print recv
if recv[:3] != '220':
    print '220 reply not received from server.'

# Sending HELO command and printing server response.
heloCommand = 'EHLO '+hostname+'\r\n'
print heloCommand
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print recv1

if recv1[:3] != '250':
    print '250 reply not received from server.'

check ='y'

while check == 'y':

    # Sending MAIL FROM command and printing server response.
    if flagm==1:
        mailFrom = raw_input("Enter the sender's email ID : ")
    mailFromCommand = 'MAIL FROM: '+mailFrom+' \r\n'
    print mailFromCommand
    clientSocket.send(mailFromCommand)
    recv2 = clientSocket.recv(1024)
    print recv2
    if recv2[:3] != '250':
        print '250 reply not received from server.'

    # Sending RCPT TO command and printing server response.
    if flagr==1:
	rcpt = raw_input("Enter the Recipient's mail ID(s) :  ")
    recipients = split(rcpt,",")
    for recipient in recipients:
        rcptToCommand = 'RCPT TO: '+recipient+'\r\n'
        print rcptToCommand
        clientSocket.send(rcptToCommand)
        recv3 = clientSocket.recv(1024)
        print recv3
        if recv3[:3] != '250':
            print '250 reply not received from server.'

    # Sending DATA command and printing server response.
    dataCommand = 'DATA\r\n'
    print "DATA\n(Enter the content of the mail)"
    clientSocket.send(dataCommand)
    recv4 = clientSocket.recv(1024)
    print recv4
    if recv4[:3] != '354':
        print '354 reply not received from server.data'

    # Sending message data.
    mailContent = raw_input()
    mailContent = '\r\n'+mailContent+'\r\n'
    clientSocket.send(mailContent)


    # Message ends with a single period.
    endCommand = '\r\n.\r\n'
    print endCommand
    clientSocket.send(endCommand)
    recv5 = clientSocket.recv(1024)
    print recv5

    flagm=1
    flagr=1
    check = raw_input("Do you want to send another mail using the same connection ? (y/n) : ")
    

# Sending QUIT command and getting the server response.
quitCommand = 'QUIT\r\n'
print quitCommand
clientSocket.send(quitCommand)
recv6 = clientSocket.recv(1024)
print recv6
if recv6[:3] != '221':
    print '221 reply not received from server.quit'
