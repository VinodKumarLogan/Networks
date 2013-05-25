#!/usr/bin/python
from socket import *
import argparse
import sys
import select
import copy
from datetime import datetime
import json
import warnings
import fcntl,os
fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK)

HOLDDOWN = 30
STABILIZATION_TIME = 30
LINK_DOWNTIME = 30

def getArgs():
    """A Parser initializer for accepting command line arguements"""
    parser = argparse.ArgumentParser(
        description="""Distance Vector Routing with split horizon and poisoned reverse""")

    parser.add_argument(
        '-i','--id', required=True, type=int, metavar='int',
        help='The Node ID')

    parser.add_argument(
        '-t','--time', required=True, type=int, metavar='int',
        help='The periodic broadcast time interval in seconds')

    parser.add_argument(
        '-e','--edge', required=True, type=str, metavar='str',
        help='The edge cost of neighbours, represented as <neigh_id:cost>, separated by commas')

    return parser.parse_args()

def acceptCLArguments():
    """A method to read command line arguments"""
    args = getArgs()
    if args.id > 15535 or args.id < 0: # or 48976 (at which point, the resultant port becomes < 1024)
        print 'The given Node ID generates an unusable port number. Please give a node id > 0 and < 15535'
        sys.exit(1)
    if args.time <= 0: # Shouldn't be 0 because, if 0, it will swamp the network with advertisements
        print 'Please give a positive value > 0 for time intervals'
        sys.exit(1)
    if len(args.edge) < 3:
        print 'Please give the edge cost of atleast one neighbour'
        sys.exit(1)
    dvtable = convertStrToDVtable(args.edge)
    if args.id in dvtable.keys():
        print 'A node cannot specify cost to reach itself'
        sys.exit(1)
    return args.id, args.time, dvtable

def convertStrToDVtable(string):
    """A method to convert a Distance Vector table in string form 
    received from command line to a dictionary form"""
    dvtable = dict()
    entries = string.split(',')
    for entry in entries:
        try:
            nodeid = int(entry[:entry.index(':')])   # key
            cost   = int(entry[entry.index(':')+1:]) # value
            dvtable[nodeid] = (cost,nodeid)
        except ValueError:
            print 'Invalid Distance Vector Table entry received:', entry
            sys.exit(1)
    return dvtable

def convertJSON_DVtable(string):
    """A method to convert a Distance Vector table in JSON stringified form 
    received from a neighbour's message/advertisement to a dictionary form"""
    tempdict = json.loads(string)
    dvtable = dict()
    for key, value in tempdict.items():
        dvtable[int(key)] = tuple(value)
    return dvtable

def getDictDiff(minuendDict, subtrahendDict):
    """Get difference between two dictionaries"""
    diffDict = dict()
    for key in minuendDict.keys():
        if not subtrahendDict.has_key(key):
            diffDict[key] = minuendDict[key]
        elif minuendDict[key] != subtrahendDict[key]:
            diffDict[key] = minuendDict[key]
    return diffDict

def setSocket(port):
    """Factory method to create a socket"""
    selfsocket = socket(AF_INET, SOCK_DGRAM)
    try:
        selfsocket.bind(('', port))
        return selfsocket
    except IOError:
        print 'Cannot bind server to port', port, '. Check whether any other program is using this port'
        sys.exit(1)

def advertise(sendsocket, neighbours, dvtable):
    """Method to periodically advertise DV or to advertise changes to DV"""
    for neighbourport in neighbours:
        neighbournodeid = neighbourport - 50000
        sendDict = copy.deepcopy(dvtable)
        for key, value in sendDict.items():
            if len(value) == 2 and value[1] == neighbournodeid and key != neighbournodeid: 
                # If the next hop is the neighbour itself, ie, the neighbour has a better route
                # that changed path (for the destination node) to go through the neighbour,
                # lie to the neighbour that you have no way of reaching the destination node
                # because, if the link from neighbour to destination node goes down, it will not try to readjust
                # itself to this source node as that will cause a loop - benefit of poisoned reverse
                sendDict[key] = (64,)
        if sendDict.has_key(neighbournodeid) and sendDict[neighbournodeid][0] == 64:
            pass
        else:
            sendsocket.sendto(json.dumps(sendDict), ('127.0.0.1',neighbourport))

def advertiser(last, interval, args):
    advertisetime = datetime.now() - last
    if advertisetime.seconds >= interval:
        advertise(*args)
        return datetime.now()
    else:
        return last

def updateAdvertiser(selfsocket, neighbours, olddvtable, dvtable):
    diffdvtable = getDictDiff(dvtable, olddvtable) # Get only updated parts of DV
    # send the updated DV to all neighbours and reset the stabilizer timer
    # as updation means that the network hasn't been stabilized yet
    advertise(selfsocket, neighbours, diffdvtable)
    updatetime = datetime.now()
    lastadvertisement = datetime.now()
    return (updatetime, lastadvertisement)

def checkStabilized(interval, lastupdated):
    timediff = datetime.now() - lastupdated
    if timediff.seconds > STABILIZATION_TIME:
        return True
    return False

def stabilizer(selfsocket, neighbours, dvtable, updated, neighboursdict, lastadvertisement):
    updatetime = datetime.now()
    linkdown = list()
    olddvtable = copy.deepcopy(dvtable)
    for neighbour in neighbours:
        neighbournodeid = neighbour-50000
        if not neighbournodeid in updated.keys() or (datetime.now() - updated[neighbournodeid]).seconds > LINK_DOWNTIME:
            # If no reply from a neighbour for a long time, assume link down
            dvtable[neighbournodeid] = (64,)
            linkdown.append(neighbour)
            for key, value in dvtable.items():
                # Check all those destinations for which the just-down link was next hop
                if len(value) == 2 and value[1] == neighbournodeid:
                    if key in neighboursdict.keys() and neighboursdict[key][0] < 64:
                        # If there is a better value in neighboursdict, take it
                        dvtable[key] = neighboursdict[key]
                    else:
                        # Otherwise, even these links are unreachable
                        # as the current node doesn't know any better alternative
                        dvtable[key] = (64,)
    for link in linkdown:
        neighbours.remove(link)
        if neighboursdict.has_key(link-50000):
            neighboursdict.pop(link-50000)

    if olddvtable != dvtable:   # If the Dv has been updated because of the neighbour's DV,
        updatetime, lastadvertisement = updateAdvertiser(selfsocket, neighbours, olddvtable, dvtable)
    print 'DV at', datetime.now(), ':', dvtable
    return (updatetime, lastadvertisement, neighbours, neighboursdict, dvtable)

if __name__ == '__main__':

    nodeid, interval, dvtable = acceptCLArguments()

    selfsocket = setSocket(nodeid+50000)

    neighbours = list()
    for key in dvtable.keys():                   # Build a list of all neighbours
        neighbours.append(key+50000)

    advertise(selfsocket, neighbours, dvtable)   # Start advertising
    updatetime = datetime.now()
    lastadvertisement = datetime.now()

    holddown = dict()
    updated = dict()

    neighboursdict = copy.deepcopy(dvtable)    

    while(True):
        try:
            inputready, outputready, errorready = select.select([selfsocket, sys.stdin], [selfsocket], [])
            for readsocket in inputready:
                if readsocket == selfsocket:
                    message, address = readsocket.recvfrom(1024)
                    neighbournodeid = address[1] - 50000
                    updated[neighbournodeid] = datetime.now()
                    if address[1] in neighbours:                   # only if the sender is a neighbour, care for his message
                        newdvtable = convertJSON_DVtable(message)  # The DV received from the neighbour
                        olddvtable = copy.deepcopy(dvtable)
                        # ^ Existing DV. If not deepcopied, will reference to the same object

                        # Processing logic for the recieved DV
                        for key in newdvtable:
                            if key not in dvtable.keys() and key != nodeid: # Learning about a new non-neighbour node
                                dvtable[key] = (newdvtable[key][0]+newdvtable[nodeid][0], neighbournodeid)
                                # ^ Cost to the newly added node will be cost to the neighbour + cost from neighbour 
                                #   to the new node. The next hop will be the neighbour 
                                if address[1] not in neighbours:
                                    neighbours.append(address[1])

                            elif key == nodeid:
                                pass
                                # Inconsistent path values to the same link not handled as in actual DV specs

                            elif dvtable[key][0] > newdvtable[key][0]+dvtable[neighbournodeid][0]:
                                # If cost to a node through this neighbour is lesser than the existing cost
                                # replace it with new cost
                                if holddown.get(key) == None or (datetime.now() - holddown[key]).seconds > HOLDDOWN:
                                    # If hold down doesn't exist for this node OR if exists, it has passed
                                    dvtable[key] = (newdvtable[key][0]+dvtable[neighbournodeid][0], neighbournodeid)
                                    
                            elif dvtable[key][0] < newdvtable[key][0]+dvtable[neighbournodeid][0] and \
                             len(dvtable[key]) == 2 and dvtable[key][1] == neighbournodeid:
                                # Value to the destination is advertised to be more
                                # The current node should care about this only when the advertiser is the next hop
                                # to the destination
                                # This case occurs when link goes down and is advertised. The value to the same
                                # destination node through the same neighbour now has a different value -
                                # in the case where a link goes down, in which case the cost goes up
                                # (due to which it won't be handled in the previous cases)
                                # length of dvtable[key] is being checked because otherwise trying to check
                                # next hop (dvtable[key][1]) sometimes can throw a KeyError
                                if key in neighboursdict.keys() and newdvtable[key][0] > neighboursdict[key][0] and \
                                 key != neighbournodeid:
                                  # This is the case where the current node had chosen an alternative path to a 
                                  # neighbour, but the link to that path is broken. Now, it has to revert back to 
                                  # the path it had replaced, which is now the best path to take
                                  # key == neighbournodeid will probably never happen. Only included for safety
                                    dvtable[key] = (neighboursdict[key][0], key)
                                elif len(newdvtable[key]) == 1:
                                    # It is the case where the destination node is not a neighbour 
                                    # (ie, not in the neighboursdict) AND the neighbour is stating that
                                    # cost to the destination node is 64 (down). So, make the entry for this link
                                    # down too
                                    dvtable[key] = (64,)
                                else:
                                    # It is the case where the destination node is not a neighbour AND 
                                    # the link is not down, but has just increased. In that case
                                    # there is no other way except accepting whatever cost increase occurs
                                    dvtable[key] = (newdvtable[key][0]+dvtable[neighbournodeid][0], neighbournodeid)
                                holddown[key] = datetime.now()
                                # There is probability of cost increase because of this block of code. So, we set a
                                # holddown time that makes sure that the DV isn't made inconsistent till the 
                                # change in the link cost is propagated throughout the network

                        if dvtable.has_key(nodeid):
                            # If the neighbour's DV has inadvertently created an entry to the current node,
                            # it has to be removed as cost to reach the same node doesn't make sense
                            dvtable.pop(nodeid)

                        if olddvtable != dvtable:   # If the Dv has been updated because of the neighbour's DV,
                            updatetime, lastadvertisement = updateAdvertiser(selfsocket, neighbours, olddvtable, dvtable)
                            
                        else:
                            if checkStabilized(interval, updatetime):
                                updatetime, lastadvertisement, neighbours, neighboursdict, dvtable = \
                                    stabilizer(selfsocket, neighbours, dvtable, updated, neighboursdict,lastadvertisement)
                            else:
                                lastadvertisement = advertiser(lastadvertisement, interval, 
                                                            args=(selfsocket, neighbours, dvtable,))

                elif readsocket == sys.stdin:
                    # This allows the user to explicitly break a link to a neighbouring node
                    try:
                        nodeno = int(sys.stdin.read())
                        if nodeno+50000 not in neighbours:
                            raise ValueError
                        dvtable[nodeno] = (64,)
                        if nodeno+50000 in neighbours:
                            neighbours.remove(nodeno+50000)
                        holddown[key] = datetime.now()
                        advertise(selfsocket, neighbours, dvtable)
                        updatetime = datetime.now()
                        lastadvertisement = datetime.now()
                    except ValueError:
                        print 'Please enter a valid node number of a neighbour'
                    except IOError:
                        print 'IOError occured'
            
            if checkStabilized(interval, updatetime):
                updatetime, lastadvertisement, neighbours, neighboursdict, dvtable = \
                    stabilizer(selfsocket, neighbours, dvtable, updated, neighboursdict, lastadvertisement)
            else:
                lastadvertisement = advertiser(lastadvertisement, interval, 
                                            args=(selfsocket, neighbours, dvtable,))
            
        except KeyboardInterrupt:
            print 'Exiting by breaking all links...'
            for key in dvtable:
                dvtable[key] = (64,)
            advertise(selfsocket, neighbours, dvtable)
            break

    selfsocket.close()