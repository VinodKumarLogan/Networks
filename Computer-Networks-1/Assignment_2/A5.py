import random
from socket import *
from argparse import *

parser = argparse.ArgumentParser()
parser.add_argument("-s","--servername", help="enter the server name. Default value is 127.0.0.1 ",default="127.0.0.1")
parser.add_argument("-p","--serverport", help="enter the serve port. Default value is 12345 ",default=12345,type=int)
parser.add_argument("-n","--packets", help="enter the number of packets to be sent .Default value is 12345 ",default=12345,type=int)

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12345))

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)

    # Capitalize the message from the client
    message = message.upper()

    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4:
        continue
    # Otherwise, the server responds serverSocket.sendto(message, address)
