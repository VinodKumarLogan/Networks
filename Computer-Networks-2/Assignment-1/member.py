import argparse,socket,sys,select

parser = argparse.ArgumentParser()
parser.add_argument("-n","--name", help="Enter the name of the chatter.")
parser.add_argument("-a","--address", help="Enter the ipv6 address of the host",default='::1')
parser.add_argument("-p","--port", help="Enter the port number through which the program exchanges data",default=12345,type=int)

args = parser.parse_args()
name = args.name # holds the chatter's name
hostAddr =  args.address # holds the host ipv6 address
hostPort =  args.port # holds the host port number

print name
print hostAddr
print hostPort

addrs = socket.getaddrinfo(hostAddr, hostPort, socket.AF_INET6, 0, socket.SOL_UDP)
ar =  addrs[0][4]
c = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
c.bind(ar)
#c.connect(ar)
c.sendto(name,ar)
print "client opened socket connection:", c.getsockname()
size = 1024
input = [c,sys.stdin]
running = 1
while running:
    inputready,outputready,exceptready = select.select(input,[],[])

    for s in inputready:

        if s == sys.stdin:
            # handle standard input
            data = sys.stdin.readline()
            msg = name+':'+data
            try:
                c.sendto(msg,(ar))
            except:
                print 'Unable to send message to the destination'
        else:
            # handle all other sockets
            data = s.recv(size)
            if data!='exit':
                print data
            else:
                s.close()
                input.remove(s)
c.close()