import argparse,sys

def validateCode(code):
	if code.count('1')+code.count('0')!=len(code):
		return False
	else:
		return True

def chippingSequence(code):
	l = list()
	for c in code:
		if c=='1':
			l.extend([1])
		else:
			l.extend([-1])
	return l

def checkST(code1,code2):
	s = 0 
	for i in range(len(code1)): #Calculating S.T
		s+=code1[i]*code2[i]
	if s==0:
		return True
	else:
		return False


def checkSTd(code1,code2):
	s = 0 
	for i in range(len(code1)): #Calculating S.T'
		s+=code1[i]*((-1)*code2[i])
	if s==0:
		return True
	else:
		return False

def checkSS(code):
	s = 0 
	for i in range(len(code)): #Calculating S.S
		s+=code[i]*code[i]
	if s!=len(code):
		return False
	s = 0 
	for i in range(len(code)): #Calculating S.S'
		s+=code[i]*((-1)*code[i])
	if s!=((-1)*len(code)):
		return False
	return True
	

def decodeSequence(code):
	s = ""
	for c in code: #Retrieving the code from the chipping sequence
		if c==1:
			s+='1'
		else:
			s+='0'
	return s

parser = argparse.ArgumentParser()
parser.add_argument("-c","--codes",required=True, help="Enter the CDMA codes ")

#parsing the arguements
args = parser.parse_args()
codes =  args.codes.split(',') # holds the codes accepted from the user

print codes

codedList = [] #Will store the chipping sequence of each code
#Validating the code
for i in range(len(codes)):
	if not validateCode(codes[i]):
		print "Code "+str(i+1)+" is invalid"
		sys.exit(0)
	else:
		codedList.append(chippingSequence(codes[i]))

print codedList

i = 0
while i<len(codedList):
	code1 = codedList[i]
	j = i + 1
	while j<len(codedList):
		code2 = codedList[j]
		if checkST(code1,code2) and checkSTd(code1,code2) and checkSS(code1) and checkSS(code2): #If S.T=0 and S.T'=0 and S.S=m and S.S'=-m
			print decodeSequence(code1)," and ",decodeSequence(code2)," are orthogonal "
		j+=1
	i+=1