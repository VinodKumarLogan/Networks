import argparse,socket,time,threading

class SendDV(threading.Thread):
    def __init__(self,t,socket,dv):
    	self.distanceVector = dv
    	self.dvRoute = socket
    	self.t = t
        threading.Thread.__init__(self)
        self.event = threading.Event()

    def run(self):
    	print "In send"
        while True:
            for key in self.distanceVector.keys():
            	if self.distanceVector[key]!=64:
            		dvRoute.sendto(str(self.distanceVector),('localhost',50000+key))
            self.sleep(self.t)

    def stop(self):
        self.event.set()

class RecvDV(threading.Thread):
    def __init__(self,nodes,socket,distanceVector):
    	self.distanceVector = distanceVector
    	self.dvRoute = socket
    	self.nodes = nodes
        threading.Thread.__init__(self)

    def run(self):
    	print "In recv"
        while True:
        	data,addr = dvRoute.recv(4096)
        	nid = int(str(addr).split(':')[1])-50000
        	if nid>0 and nid<nodes+1:
        		dvNeigh = {}
        		data = data[1:-1]
        		for neigh in data.split(","):
        			n = neigh.split(":")
        			dvNeigh[int(n[0])] = int(n[1])
        		print "Distance Vector from ",nid,dvNeigh

    def stop(self):
        self.event.set()



parser = argparse.ArgumentParser()
parser.add_argument("-i","--nodeid", required=True, help="Enter the node number",type=int)
parser.add_argument("-n","--nodes", required=True, help="Enter the number of nodes in the network",type=int)
parser.add_argument("-t","--time", required=True, help="Enter the periodic broadcast time",default=3,type=int)
parser.add_argument("-e","--edgecost", required=True, help="Enter the edge costs for each neighbour")
#parsing the arguements
args = parser.parse_args()
nodeId = args.nodeid # holds the node id
broadcastTime =  args.time # holds the periodic broadcast time
neighCost =  args.edgecost # holds the edge cost of each neighbour
nodes =  args.nodes # holds the number of nodes in the network

#Printing the details of the parameters
print 'Node ID : ',nodeId
print 'Periodic Broadcast time : ',broadcastTime
distanceVector = {}
for neigh in neighCost.split(","):
	n = neigh.split(":")
	distanceVector[int(n[0])] = int(n[1])

print "NodeID Cost"
for i in range(1,nodes+1):
	try:
		if distanceVector[i]>0:
			print i,"  \t",distanceVector[i]
	except:
		if i!=nodeId:
			distanceVector[i] = 64
			print i,"  \t",distanceVector[i]

print 'Distance Vector : ',distanceVector

dvRoute = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #Creating the socket
dvRoute.bind(('localhost',50000+nodeId)) #Binding the socket to the localhost and the port number
print "Socket Created",dvRoute
send = SendDV(broadcastTime,dvRoute,distanceVector)
send.start()
recv = RecvDV(nodes,dvRoute,distanceVector)
recv.start()