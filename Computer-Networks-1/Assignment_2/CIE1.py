import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-f","--filesize", help="enter the filesize in MBytes. Default value is 12.5MB",default=12.5,type=float)
parser.add_argument("-p","--packetsize",help="enter the size of each packet in Mbits",default=1,type=float)
parser.add_argument("-a","--transmissionspeeda",help="enter the transmission speed of link 1 (A to sw-1)]: in Mbps ",default=1,type=float)
parser.add_argument("-b","--transmissionspeedb",help="enter the transmission speed of link 2 (sw-1 to sw-2)]: in Mbps ",default=1,type=float)
parser.add_argument("-c","--transmissionspeedc",help="enter the transmission speed of link 3 (sw-2 to sw-3)]: in Mbps ",default=2,type=float)
parser.add_argument("-d","--transmissionspeedd",help="enter the transmission speed of link 4 (sw-3 to B)]: in Mbps ",default=1,type=float)
parser.add_argument("-A","--cutthrough1",help="enter the number of bits for cut through switching for sw1 ",default=0)
parser.add_argument("-B","--cutthrough2",help="enter the number of bits for cut through switching for sw2 ",default=10000)
parser.add_argument("-C","--cutthrough3",help="enter the number of bits for cut through switching for sw3 ",default=0)

args = parser.parse_args()
fs = args.filesize
ps = args.packetsize
tspeed1 = args.transmissionspeeda
tspeed2 = args.transmissionspeedb
tspeed3 = args.transmissionspeedc
tspeed4 = args.transmissionspeedd
cut1 = args.cutthrough1
cut2 = args.cutthrough2
cut3 = args.cutthrough3

t=0.0
n = float(fs*8)/float(ps)
i=1
print "Pk#     Sw-1     Sw-2     Sw-3     Dest"
while n>=i:
    td1=t+(float(ps)/float(tspeed1))
    if cut1!=0:
        td2=(float(cut1)/float(tspeed2*(10**6))) 
    else:
        td2=(float(ps)/float(tspeed2)) 
    if cut2!=0:
        td3=(float(cut2)/float(tspeed3*(10**6))) 
    else:
        td3=(float(ps)/float(tspeed3)) 
    if cut3!=0:
        td4=(float(cut3)/float(tspeed4*(10**6))) 
    else:
        td4=(float(ps)/float(tspeed4))
    t=max(td1,td2,td3,td4)
    td2=td1+td2
    td3=td2+td3
    td4=td4+td3
    print str(i)+"     "+str(td1)+"      "+str(td2)+"     "+str(td3)+"     "+str(td4)
    i=i+1
