#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2013 liudanking

import sys
from gevent import socket
import time
import struct
import serial

def getobdsimData(ser):
	pid=['0101',
		 '0102',
		 '0104',
		 '0105',
		 '010B',
		 '010C',
		 '010D',
		 '010E',
		 '010F',
		 '0110',
		 '0111',
		 '011F',
		 '0121',
		 '012F',
		 '0131',
		 '0142',
		 '0146',
		 '0151',
		 '015A']
	print pid
	ret_char = '\15'
	

	piddata = [i for i in range(len(pid))]
	for i in range(len(pid)):
		ser.write(pid[i]+ret_char)
		ret = ''
		while True:
			ch = ser.read()
			if (ch!='>'):
				ret += ch
			else:
				break
		ret = "".join(ret.split())
		print ret, len(ret)
		if ret[len(ret)-6:]=='NODATA' or len(ret)==5 and ret[4]=='?':
			piddata[i] = 0
		else:
			ret = ret[8:]
			if len(ret) > 4:
				ret = ret[-4:]
			elif len(ret) == 3:
				ret = ret[-2:]
			piddata[i] = int(ret,16)

			
	print piddata
	return piddata

# connect init
address = ('vanet.fenhetech.com', 9001)
sock = socket.socket(type=socket.SOCK_DGRAM)
ser = serial.Serial('COM20', 38400)

while True:
	access_token = '7317f1835d472ad1'
	token_char = [int(access_token[i:i+2],16) for i in range(0,15,2)]
	print len(token_char)
	access_token = [struct.pack('=B',token_char[i]) for i in range(0,8)]
	token = ''
	for ch in access_token:
		token += ch
	print token
	fmt = '=BB8sffBHBBBHBBBHBHHBHHBBB'
	piddata = getobdsimData(ser)
	message = struct.pack(fmt,13,
							1,
							token,
							12.34543222,
							180.26754,
							piddata[0],
							piddata[1],
							piddata[2],
							piddata[3],
							piddata[4],
							piddata[5],
							piddata[6],
							piddata[7],
							piddata[8],
							piddata[9],
							piddata[10],
							piddata[11],
							piddata[12],
							piddata[13],
							piddata[14],
							piddata[15],
							piddata[16],
							piddata[17],
							piddata[18])
						
	#print message, 'len:', len(message)
	message = struct.pack('=H', len(message)) + message
	#message = message[:20]
	#print message, 'len:', len(message)

	print 'Sending %s bytes to %s:%s' % ((len(message), ) + address)
	sock.sendto(message, address)
	data, address = sock.recvfrom(8192)
	print '%s:%s: got %r' % (address + (data, ))
	time.sleep(10)