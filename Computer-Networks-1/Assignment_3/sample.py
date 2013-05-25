import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-N","--packets", help="Enter the total numnber of packets to be sent(minimum 20). Default value is 20 ",default=20,type=int)
parser.add_argument("-t","--timeout", help="Enter the timeout value in seconds. Default value is 2s ",default=2,type=int)
parser.add_argument("-s","--serverip", help="Enter the server's IP address. Default value is 127.0.0.1",default="127.0.0.1")
parser.add_argument("-p","--serverport", help="Enter the server's port number. Default value is 12345",default=12345)
parser.add_argument("-w","--windowsize", help="Enter the congestion window's size. Default value is 4",default=4,type=int)
#parser.add_argument("-l","--packetloss", help="Enter the average packet loss as percentage.Default value is 30%",default=30,type=int)

args = parser.parse_args()

