#!/usr/bin/env python

"""
An echo server that uses select to handle multiple clients at a time.
Entering any line of input at the terminal will exit the server.
"""

import select
import socket
import sys

host = '::1'
port = 50000
backlog = 5
size = 1024
addrs = socket.getaddrinfo("::1", port, socket.AF_INET6, 0, socket.SOL_TCP)
ar =  addrs[0][4]
server = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
server.bind(ar)

server.listen(5)
input = [server,sys.stdin]
running = 1
while running:
    inputready,outputready,exceptready = select.select(input,[],[])

    for s in inputready:

        if s == server:
            # handle the server socket
            client, address = server.accept()
            input.append(client)

        elif s == sys.stdin:
            # handle standard input
            junk = sys.stdin.readline()
            running = 0 

        else:
            # handle all other sockets
            data = s.recv(size)
            if data:
                print 'Received Data : ',data
                s.send(data.upper())
            else:
                s.close()
                input.remove(s)
server.close()