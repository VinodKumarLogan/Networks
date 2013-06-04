from socket import *
import ssl

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = "smtp.gmail.com"
port = 587

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
ssl_clientSocket = ssl.wrap_socket(clientSocket, 
        ca_certs = '/etc/ssl/certs/ca.pem',
        cert_reqs = ssl.CERT_REQUIRED,ssl_version=ssl.PROTOCOL_SSLv23) 
ssl_clientSocket.connect((mailserver, port))

###################################################################
print "got to here 1"
###############################################################

recv = ssl_clientSocket.recv(1024)
print
print recv

# If the first three numbers of what we receive from the SMTP server are not
# '220', we have a problem
if recv[:3] != '220':
    print '220 reply not received from server.'

# Send HELO command and print server response.
heloCommand = 'EHLO \r\n'
ssl_clientSocket.send(heloCommand)
recv1 = ssl_clientSocket.recv(1024)
print recv1

######################################################################
print "Got to here 2"
#####################################################################

# If the first three numbers of the response from the server are not
# '250', we have a problem
if recv1[:3] != '250':
    print '250 reply not received from server.'

# Send MAIL FROM command and print server response.
mailFromCommand = 'MAIL From: vinodgoku@gmail.com\r\n'
ssl_clientSocket.send(mailFromCommand)
recv2 = ssl_clientSocket.recv(1024)
print recv2

# If the first three numbers of the response from the server are not
# '250', we have a problem
if recv2[:3] != '250':
    print '250 reply not received from server.'

# Send RCPT TO command and print server response.
rcptToCommand = 'RCPT To: vinodgoku@gmail.com\r\n'
ssl_clientSocket.send(rcptToCommand)
recv3 = ssl_clientSocket.recv(1024)
print recv3

# If the first three numbers of the response from the server are not
# '250', we have a problem
if recv3[:3] != '250':
    print '250 reply not received from server.'

# Send DATA command and print server response.
dataCommand = 'DATA\r\n'
ssl_clientSocket.send(dataCommand)
recv4 = ssl_clientSocket.recv(1024)
print recv4

# If the first three numbers of the response from the server are not
# '250', we have a problem
if recv4[:3] != '250':
    print '250 reply not received from server.'

# Send message data.
ssl_clientSocket.send(msg)

# Message ends with a single period.
ssl_clientSocket.send(endmsg)

# Send QUIT command and get server response.
quitCommand = 'QUIT\r\n'
ssl_clientSocket.send(quitCommand)
recv5 = ssl_clientSocket.recv(I1024)
print recv5

# If the first three numbers of the response from the server are not
# '250', we have a problem
if recv5[:3] != '221':
    print '221 reply not received from server.'
