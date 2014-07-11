#!/usr/bin/env python
# encoding: utf-8

import struct
import serial
import time


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
ser = serial.Serial('COM20', 38400)

piddata = [i for i in range(len(pid))]
print piddata
while True:
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
			piddata[i] = int(ret,16)

			
	print piddata
	
	time.sleep(10)


for i in range(0, 2):
    print ser.write('0104\15')
    ret = ''
	while True:
		ch=ser.read()
		ret+=ch
		if (ch=='>'):
			break
print 'ok:', ret, len(ret)