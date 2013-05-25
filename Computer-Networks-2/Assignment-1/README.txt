ASN1
----
Group Members
-------------
Shrikrishna Holla 1PI10IS100
Vinod Kumar L     1PI10IS118
Ashish Shetty     1PI10IS132

Question
---------
B1. Implement 3-party chat using UDP based on IPv6. For the program specify the command
line arguments as follows
-n <name of chatter>
-a <ipv6 address to be used by this program>
-p <port number on which this program will receive chat msgs from others>
-d <ipv6 address of 2nd party>,<ipv6 address of 3rd party>
-r <port number of 2nd party>,<port number of 3rd party>
The program will receive inputs on command line and send the same to other chat partners.
When the program receives the input from other chat partners, it should display the same on
console along with its id.

Run the program using this command:
python asn1.py -n ... [command line arguesments]

Implementation
---------------
*The program asn1.py implements a 3-party  chat using UDP based on IPv6. This program should be run on all the 3 systems to chat successfully.
 The program takes user's name,IPv6 address,Port number and IPv6 addresses and corresponding port numbers of the other two members as command
 line arguements. Usage of the flags is best described by the -h or --help option.
*We check if the number of arguements are correct and handle exceptions if the Arguements are invalid.
*socket.getaddrinfo() collects the host details in a tuple and a socket is created and bound to the port number
*select.select() is used to check whether the data arriving is from any of the sockets or the standard input, so that, the one arriving from stdin is send to other 2 members and the other one is received at the socket using recv function and finally displayed on the console. 
*fcntl.fcntl(sys.stdin, fcntl.F_SETFL, os.O_NONBLOCK) is used to set the stdin to non blocking mode
 We did this to receive a message even when the user is in the middle of typing his message and at the same time retain the message in the buffer.
*Once the user enters '\n' , the message is sent to both the receipients and is displayed on their console along with the senders's name .
*To quit the chat , user has to enter 'exit\n'.

Challenges Faced
----------------
*It was difficult to receive a message while the user was in the middle of typing his own message. We were able to achieve this , but the message
 that has already been entered by the user is in the buffer but not displayed on the screen once again. This is because stdin is line buffered 
 input. so the user has to continue from where he left off.
*Testing was cumbersome because we used conventional, long IPv6 addresses.
  
We have uploaded 3 more text files regarding our Understanding and Contribution to the program
