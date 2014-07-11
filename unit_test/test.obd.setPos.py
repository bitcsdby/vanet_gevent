#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2013 liudanking

import sys
from gevent import socket
import time
import struct

current_time = time.time()
def make_msg():
	global current_time
	current_time = current_time + 1
	#message = struct.pack('=BBQddIff', 11, 1, 2013, 1.5, 1.5, current_time, 80.1, 90.1)
	#print message, 'len:', len(message)
	#message = struct.pack('H', len(message)) + message
	#message = message[:20]
	message = struct.pack('=40B',0x26,0x00,0x0b,0x00,0x73,0x17,0xf1,0x83,0x5d,0x47,0x2a,0xd1,0xdb,0xf9,0x7e,0x6a,0xbc,0x97,0xaa,0x40,0xf0,0xa7,0xc6,0x4b,0xb7,0xde,0xc6,0xc0,0x00,0xe7,0x47,0x48,0x33,0x33,0xf3,0x3f,0x33,0x73,0xa8,0x43)
	print message, 'len:', len(message)
	return message
	
"""
message = struct.pack('=BBQddIff', 11, 1, 2013, 1.5, 1.5, 1345678334, 80.1, 90.1)
print message, 'len:', len(message)
message = struct.pack('H', len(message)) + message
#message = message[:20]
print message, 'len:', len(message)
"""
#address = ('vanet.fenhetech.com', 9001)
#address = ('localhost', 9001)
address = ('www.ecloudan.com', 9001)
sock = socket.socket(type=socket.SOCK_DGRAM)
#print 'Sending %s bytes to %s:%s' % ((len(message), ) + address)
while True:
	message = make_msg()
	sock.sendto(message, address)
	#data, address = sock.recvfrom(8192)
	#print '%s:%s: got %r' % (address + (data, ))
	time.sleep(1)