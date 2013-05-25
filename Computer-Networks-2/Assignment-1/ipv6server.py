import socket
 
port = 12345
addrs = socket.getaddrinfo("::1", port, socket.AF_INET6, 0, socket.SOL_TCP)
ar =  addrs[0][4]
s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
s.bind(ar)
s.listen(1)
print "server opened socket connection:"
while True:
    conn, addr = s.accept()
    print 'Server: Connected by', addr
    data = conn.recv(1024)
    conn.send(data)
    conn.close() 