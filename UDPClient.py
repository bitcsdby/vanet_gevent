# Copyright (c) 2013 liudanking
"""Send a datagram to localhost:9000 and receive a datagram back.

Usage: python udp_client.py MESSAGE

Make sure you're running a UDP server on port 9000 (see udp_server.py).

There's nothing gevent-specific here.
"""
import sys
from gevent import socket
import time

address = ('vanet.fenhetech.com', 9001)
message = 'we will rock you' #' '.join(sys.argv[1:])
sock = socket.socket(type=socket.SOCK_DGRAM)
#sock.connect(address)
print 'Sending %s bytes to %s:%s' % ((len(message), ) + address)

while True:
	sock.sendto(message, address)
	data, address = sock.recvfrom(8192)
	print '%s:%s: got %r' % (address + (data, ))
	time.sleep(1)
