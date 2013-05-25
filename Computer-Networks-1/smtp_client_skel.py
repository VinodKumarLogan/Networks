#smtp_client_skel.py

from socket import *
from sys import *

# Choosing localhost as the default mail server
mailserver = 'smtp.gmail.com'
serverPort = 587

# Creating socket called clientSocket and establishing a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
  ssl_clientSocket = ssl.wrap_socket(clientSocket,
          ca_certs = '/etc/ssl/certs/ca.pem',
          cert_reqs = ssl.CERT_REQUIRED)
  ssl_clientSocket.connect((mailserver, serverPort))
#clientSocket.connect((mailserver, serverPort))
recv = clientSocket.recv(1024)
print recv
if recv[:3] != '220':
    print '220 reply not received from server.'
else:
    print 'success socket connection\n'

# Sending HELO command and printing server response.
heloCommand = 'EHLO vinod\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print recv1

if recv1[:3] != '250':
    print '250 reply not received from server.'
else:
    print 'success helo\n'

# Sending MAIL FROM command and printing server response.
mailFromCommand = 'MAIL FROM: <vinod@pes.edu>\r\n'
clientSocket.send(mailFromCommand)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '250':
    print '250 reply not received from server.'
else:
    print 'success mail from\n'

# Sending RCPT TO command and printing server response.
rcptToCommand = 'RCPT TO: root\r\n'
clientSocket.send(rcptToCommand)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '250':
    print '250 reply not received from server.'
else:
    print 'success rcpt to\n'


# Sending DATA command and printing server response.
dataCommand = 'DATA\r\n'
clientSocket.send(dataCommand)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '354':
    print '354 reply not received from server.data'
else:
    print 'success data\n'


# Sending message data.
mailContent = '\r\nHello Vinod\r\n'
clientSocket.send(mailContent)
#recv1 = clientSocket.recv(1024)
#print recv1
#if recv1[:3] != '250':
#    print '250 reply not received from server.'
#else:
#    print 'success content\n'


# Message ends with a single period.
endCommand = '\r\n.\r\n'
clientSocket.send(endCommand)
#recv1 = clientSocket.recv(1024)
#print recv1
#if recv1[:3] != '250':
#    print '250 reply not received from server.'
#else:
#    print 'success period\n'

# Sending QUIT command and getting the server response.
quitCommand = 'QUIT\r\n'
clientSocket.send(quitCommand)
recv1 = clientSocket.recv(1024)
print recv1
if recv1[:3] != '221':
    print '221 reply not received from server.quit'
else:
    print 'success quit\n'

