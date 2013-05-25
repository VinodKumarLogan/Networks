import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("-d","--distance", help="enter the distance between any two tollbooth in Km. Default value is 100 ",default=100)
parser.add_argument("-s","--caravanspeed", help="enter the average speed at which the caravan travels in Km/hr. Default value is 80 Km/hr ",default=80)
parser.add_argument("-p","--processingdelay", help="enter the processing delay of each car at the tollbooth in seconds . Default value is 10 ",default=10,type=float)
parser.add_argument("-c","--cars", help="enter the number of cars in the caravan. Default value is 10 ",default=10,type=int)
parser.add_argument("-n","--tollbooths", help="enter the number of tollbooths. Default value is 2 ",default=2,type=int)
args = parser.parse_args()
dist = args.distance
speed = args.caravanspeed
pdelay = args.processingdelay
car = args.cars
toll = args.tollbooths

totaldelay=((float(dist)/float(speed))*3600+(pdelay*car))*toll
h=int(totaldelay/3600)
print totaldelay
m=int((totaldelay-(3600*h))/60)
s=int(totaldelay-(3600*h)-(60*m))
print "Total time delay = "+str(h)+" hours "+str(m)+" mins "+str(s)+" seconds "
