# Copyright (c) 2013 liudanking
"""Send a datagram to localhost:9000 and receive a datagram back.


#24 00	0C	00	73 17 F1 83 5D 47 2A D1	00	00 00	7F	7F	7F	FF 7F	7F	7F	7F	FF 7F	7F	41 0F	00 00	7F	09 00	FF 30	7F	01	7F

#24 00	0C	00	73 17 F1 83 5D 47 2A D1	00	00 00	2C	FF	FF	0A F0	1C	FF	FF	FF F4	FF	01 40	30 00	15	0DA0	89 F3	FF	FF	32

#24 00	0C	00	73 17 F1 83 5D 47 2A D1	88	88 88	88	FF	FF	88 88	88	FF	FF	88 88	FF	88 88	88 88	88	88 88	88 88	FF	FF	88


Usage: python udp_client.py MESSAGE

Make sure you're running a UDP server on port 9000 (see udp_server.py).

There's nothing gevent-specific here.
"""
import sys
from gevent import socket
import time

#address = ('vanet.fenhetech.com', 9001)
address = ('localhost',9001)
message1 = '\24\00\x0C\00\73\17\xF1\x83\x5D\47\x2A\xD1\00\00\00\x2C\xFF\xFF\x0A\xF0\x1C\xFF\xFF\xFF\xF4\xFF\x01\x40\x30\x00\x15\x0D\xA0\x89\xF3\xFF\xFF\x32'

message2 = '\24\00\x0C\00\73\17\xF1\x83\x5D\47\x2A\xD1\x88\x88\x88\x88\xFF\xFF\x88\x88\x88\xFF\xFF\x88\x88\xFF\x88\x88\x88\x88\x88\x88\x88\x88\x88\xFF\xFF\x88'

sock = socket.socket(type=socket.SOCK_DGRAM)
#sock.connect(address)
print 'Sending %s bytes to %s:%s' % ((len(message2),) + address)

while True:
	sock.sendto(message2, address)
	#data, address = sock.recvfrom(8192)
	#print '%s:%s: got %r' % (address + (data, ))
	time.sleep(1)
	
