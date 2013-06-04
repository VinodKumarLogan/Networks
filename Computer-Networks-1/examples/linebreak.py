flag=1
y=""
while flag==1:
    x=raw_input()
    y+=x+'\n'
    if x[:1] is '.':
        flag=0
print y
