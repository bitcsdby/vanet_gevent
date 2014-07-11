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
	message = struct.pack('=15B',0x0d,0x00,0xff,0x00,0x73,0x17,0xf1,0x83,0x5d,0x47,0x2a,0xd1,0x09,0x44,0x79) 
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