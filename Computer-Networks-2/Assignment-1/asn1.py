import argparse,socket,sys,select,threading,fcntl,os
#fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)

parser = argparse.ArgumentParser()
parser.add_argument("-n","--name", required=True, help="Enter the name of the chatter.")
parser.add_argument("-a","--hostadd", required=True, help="Enter the ipv6 address of the host",default='::1')
parser.add_argument("-p","--hostport", required=True, help="Enter the port number through which the program exchanges data",default=12345,type=int)
parser.add_argument("-d","--destinationip", required=True, help="Enter the destination of chatter 1 (<ipv6add1>,<ipv6ad2>)")
parser.add_argument("-r","--destinationport", required=True, help="Enter the destination of chatter 1 (<port1>,<port2>)")
#parsing the arguements
args = parser.parse_args()
name = args.name # holds the chatter's name
hostAddr =  args.hostadd # holds the host ipv6 address
hostPort =  args.hostport # holds the host port number
destinationip =  [ip.strip() for ip in args.destinationip.split(",")] # holds the chatter 1's ipv6 add and port number
destinationport =  [port.strip() for port in args.destinationport.split(",")] # holds the chatter 2's ipv6 add and port number

if len(destinationip) != 2 and len(destinationport) != 2:
    print 'Please provide two destination IPs and corrresponding destination ports for 3-way chat'
    sys.exit(0)

#Printing the details of the parameters
print 'Name of the chatter is ',name
print 'Host IPV6 address : ',hostAddr
print 'Host port number : ',hostPort
print 'Destination 1 IPV6 address : ',destinationip[0],' Port : ',destinationport[0]
print 'Destination 2 IPV6 address : ',destinationip[1],' Port : ',destinationport[1]

size = 1024
addrs = socket.getaddrinfo(hostAddr, hostPort, socket.AF_INET6, 0, socket.SOL_UDP) #Retrieving the IPV6 address' details
ar =  addrs[0][4] #Tuple containing IPV6 address,port number,
chat = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) #Creating the socket
chat.bind(ar) #Binding the socket to the host IPV6 address

#Retreiving the IPV6 address' details
try:
    addrs1 = socket.getaddrinfo(destinationip[0], int(destinationport[0]), socket.AF_INET6, 0, socket.SOL_UDP)
    ar1 =  addrs1[0][4]
except:
    print 'Invalid Destination 1 Credentials'

#Retreiving the IPV6 address' details
try:
    addrs2 = socket.getaddrinfo(destinationip[1], int(destinationport[1]), socket.AF_INET6, 0, socket.SOL_UDP)
    ar2 =  addrs2[0][4]
except:
    print 'Invalid Destination 1 Credentials'

print '************************STARTING 3-PARTY IPV6 CHAT************************ '
print 'Me: ',
sys.stdout.flush()
inp = [chat,sys.stdin]
running = True
senddata = ''
while running:
    #Wait for any input to be received from stdin or any of the clients
    inputready,outputready,exceptready = select.select(inp,[],[])
    #sys.stdout.write('ME : ')
    #lock = threading.Lock()
    for s in inputready:
        if s == sys.stdin: #If the input received is from the stdin , the message needs to be forwarded to other sockets
            #lock.acquire()
            #try:
            try:
                senddata = sys.stdin.read()
            except IOError:
                print 'error'
                pass
            if senddata=='exit\n':
                running = False
                break
            try:
                chat.sendto(name+':'+senddata,ar1)
            except:
                print 'Unable to send message to destination1'
            try:
                chat.sendto(name+':'+senddata,ar2)
                senddata = ''
            except:
                print 'Unable to send message to destination2'
                senddata = ''
            finally:
                sys.stdout.write('Me: ')
                sys.stdout.flush()
            #finally:
            #    lock.release()
        else:
            # handle all other sockets
            #lock.acquire()
            #try:
            recvdata = chat.recv(size)
            if recvdata!='exit\n':
                print
                print recvdata
                try:
                    print 'Me: ',sys.stdin.read(),
                    sys.stdout.flush()
                except IOError:
                    pass
            else:
                running = False
                break
            #finally:
            #    lock.release()

print '************************ENDING 3-PARTY IPV6 CHAT************************ '
chat.close()
