#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2013 liudanking

import sys
from gevent import socket
import time
import struct
import json

def make_loginstring():
	loginstring = json.dumps({'sn':'user1', 'pw':'pw1'})
	message = struct.pack('=BB', 10, 1) + loginstring
	message = struct.pack('=H', len(message)) + message
	print message
	return message
	
address = ('vanet.fenhetech.com', 9001)
sock = socket.socket(type=socket.SOCK_DGRAM)
#print 'Sending %s bytes to %s:%s' % ((len(message), ) + address)
while True:
	message = make_loginstring()
	sock.sendto(message, address)
	data, address = sock.recvfrom(8192)
	print '%s:%s: got %r' % (address + (data, ))
	time.sleep(1)