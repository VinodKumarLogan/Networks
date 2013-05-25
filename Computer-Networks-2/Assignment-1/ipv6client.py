import socket
 
port = 50000
addrs = socket.getaddrinfo("::1", port, socket.AF_INET6, 0, socket.SOL_TCP)
ar =  addrs[0][4]
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.connect(ar)
print "client opened socket connection:", s.getsockname()
while True:
	data = raw_input('Enter the data to be sent : ')
	s.send(data)
	if data=='exit':
		break
	data = s.recv(1024)
	print 'Client received response:', repr(data)
s.close()