#program to display use of sys.argv[]
import sys
i=1
print "The program name is ", sys.argv[0]
while i< len(sys.argv):
    print "The ",i," argument is", sys.argv[i]
    i+=1
