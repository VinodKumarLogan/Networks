import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-d","--distance", help="enter the link distance in Km. Default value is 10000 ",default=10000)
parser.add_argument("-t","--transmissionspeed", help="enter the transmission speed of the link in Mbps. Default value is 1Mbps ",default=1)
parser.add_argument("-p","--propagationspeed", help="enter the propagation speed in 10^8 m/sec . Default value is 2x10^8 m/sec ",default=2,type=float)
parser.add_argument("-f","--filesize", help="enter the filesize in MBytes. Default value is 10 ",default=10)
parser.add_argument("-a","--acknowledgement", help="enter the size of acknowledgement packet in bytes. Default value is 125 ",default=125,type=int)
parser.add_argument("-s","--packetsize",help="enter the size of each packet in bytes",default=2000)
args = parser.parse_args()
dist = args.distance
tspeed = args.transmissionspeed
pspeed = args.propagationspeed
fs = args.filesize
ack = args.acknowledgement
ps = args.packetsize

pdelay = 2*float(dist*1000)/float(pspeed*10**8)
tdelay = float(ps+ack)*8/float(1000000*tspeed)
print pdelay
print tdelay
totaldelay = ((fs*1000000)/ps)*(pdelay+tdelay)
print "Total time delay = "+str(totaldelay)+"s"
