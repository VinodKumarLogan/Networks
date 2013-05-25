import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s","--servername", help="enter the server name. Default value is 127.0.0.1 ",default="127.0.0.1")
parser.add_argument("-p","--portno", help="enter the port number. Default value is 25 ",default=25,type=int)
parser.add_argument("-n","--hostname", help="enter the host name. Default value is localhost ",default="localhost")
parser.add_argument("-m","--mailid", help="enter the sender's email id")
args = parser.parse_args()
print args.servername,"\n"
print args.portno,"\n"
print args.hostname,"\n"
print args.mailid,"\n"
