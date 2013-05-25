import argparse 

def fact(n):
    f=i=1
    if n!=0:
        for i in range(n):
            i=i+1
            f=f*i
    return f 

def combination(n,r):
    f1=fact(n)
    f2=fact(r)
    f3=1
    if (n-r)!=0:
        f3 = fact(n-r)
    comb = f1/(f2*f3)
    return comb 

parser = argparse.ArgumentParser()
parser.add_argument("-l","--linkspeed", help="enter the speed of the link . Default value is 3 ",default=3,type=float)
parser.add_argument("-s","--userspeed", help="enter the speed at which the user transmits data  . Default value is 1 ",default=1,type=float)
parser.add_argument("-p","--percentageusage", help="enter the average percent of time during which the user will be transmitting . Default value is 10 ",default=10,type=float)
parser.add_argument("-u","--users", help="enter the total number of users sharing the link. Default value is 4 ",default=4,type=int)
args = parser.parse_args()
link = args.linkspeed
user = args.users
speed = args.userspeed
usage = args.percentageusage

i=1
for i in range(user):
    prob = 0
    j=1
    i = i + 1
    if (link/speed)>=i:
        for j in range(i):
              prob=prob+(combination(user,j)*((usage/100)**j)*((1-(usage/100))**(user-j)))
              j =j +1
        print "Probabilty of upto "+str(i)+" users are transmitting (without) is "+str(prob)
