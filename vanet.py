#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2013 liudanking

import gevent
import struct
import time
import json
from common import *
from config import *
import traceback

from statistic import Statistic

# import log module
import log
import logging

accdict = {}

# process the standard packet
def packet_handler(client_socket, address, data_packet, stype='tcp'):# parse packet
    #print data_packet
    pack_len, pack_type, pack_extras = struct.unpack('HBB', data_packet[:4])
    data_content = data_packet[4:]
    #print 'length: %d, type: %d, extras: %d' % (pack_len, pack_type, pack_extras)

    res_data = ''  # process packet
    if pack_type == 10:		# login
        print 'loging request'
        url = ConfigAPI['base_url'] + 'vanet.auth.obd.getToken'
        res_data = call_http_api(url, data_content, 'post')
    elif pack_type == 11:		# gps data upload
        print 'gps data upload'
        url = ConfigAPI['base_url'] + 'vanet.obd.setPos'
        fmt = '=Qddiff'
        fmt_size = struct.calcsize(fmt)  # print fmt_size, len(data_content)
        if fmt_size != len(data_content):
            pack_extras = 1
            res_data = response_json_error('packet struct invalid')
            logging.info(res_data)
        else:
            pid, longtitude, latitude, gps_time, speed, course = struct.unpack(fmt, data_content)
            access_token = ''
            num_chars = struct.unpack('=8B',data_content[:8])
            for ch in num_chars:
                access_token += '%02x'% ch
            post_data = {'access_token': access_token,
                         'longtitude': longtitude,
                         'latitude': latitude,
                         'gps_time': gps_time+8*3600,
                         'speed': speed,
                         'course': course}   # print post_data
            post_data = json.dumps(post_data)
            res_data = call_http_api(url, post_data, 'post')
    elif pack_type == 12:  # obd data upload
        #print 'obd data upload'
        url = ConfigAPI['base_url'] + 'vanet.obd.setBaseData'
        fmt = '=QBHBBBHBBBHBHHBHHBBB'
        fmt_size = struct.calcsize(fmt)
        #print fmt_size, len(data_content)
        if (fmt_size != len(data_content)):
            pack_extras = 1
            res_data = response_json_error('packet struct invalid')
            logging.info(res_data)
        else:
            obd_data = struct.unpack(fmt, data_content)
            access_token = ''
            num_chars = struct.unpack('=8B', data_content[:8])
            for ch in num_chars:
                access_token += '%02x'% ch
            post_data = {'access_token':access_token,\
                         'DTC_CNT': obd_data[1],\
                         'DTCFRZF': obd_data[2],\
                         'LOAD_PCT': obd_data[3],\
                         'ECT': obd_data[4],\
                         'MAP': obd_data[5],\
                         'RPM': obd_data[6],\
                         'VSS': obd_data[7],\
                         'SPARKADV': obd_data[8],\
                         'IAT': obd_data[9],\
                         'MAF': obd_data[10],\
                         'TP': obd_data[11],\
                         'RUNTM': obd_data[12],\
                         'MIL_DIST': obd_data[13],\
                         'FLI': obd_data[14],\
                         'CLR_DIST': obd_data[15],\
                         'VPWR': obd_data[16],\
                         'AAT': obd_data[17],\
                         'FUEL_TYP': obd_data[18],\
                         'APP_R':obd_data[19]}
            #print access_token
            if post_data['VSS'] == 0x88:  # invalid data
                print 'invalid data'
                if accdict.has_key(access_token) and accdict[access_token] != -1:
                    accdict[access_token] += 1;
                else:
                    print 'Still Stop!!!!!!!!'
                    accdict[access_token] = -1;
                if accdict[access_token] >= 4:
                	accdict[access_token] = -1
                	eptdict = {'access_token':access_token}
                	urlpull = ConfigAPI['base_url'] + 'vanet.obd.getTripobddata'
                	eptdict = call_http_api(urlpull,json.dumps(eptdict),'post')
                	try:
                            eptdict = json.loads(eptdict)
                            s = Statistic(access_token)
                            if eptdict.has_key('msg'):
                                if type(eptdict['msg']) == type([]):
                                    print 'Valid trip data!!!!!!!!!'
                                    s.dbitems = eptdict['msg']
                                    sitem = s.runstatistic()
                			
                        	    sitem = json.dumps(sitem)
                        	    urlpush = ConfigAPI['base_url'] + 'vanet.obd.addTrip'
                                    print urlpush
                                    res_data = call_http_api(urlpush,sitem,'post')
                                    print res_data
                                else:
                                    print 'Server Error! No Data Info !!!!!!!!!'
    			except:
    				print 'Invalid Data!!'               
            else:
                accdict[access_token] = 0; # valid data
            #print post_data
            post_data = json.dumps(post_data)
            #print post_data
            res_data = call_http_api(url, post_data, 'post')
    elif (pack_type == 13):		# gps and pbd data upload
        print 'gps, obd data upload'
        url = ConfigAPI['base_url'] + 'vanet.obd.setMainData'
        fmt = '=QffBHBBBHBBBHBHHBHHBBB'
        fmt_size = struct.calcsize(fmt)
        #print fmt_size, len(data_content)
        if (fmt_size != len(data_content)):
            pack_extras = 1
            res_data = response_json_error('packet struct invalid')
            logging.info(res_data)
        else:
            obd_data = struct.unpack(fmt, data_content)
            access_token = ''
            num_chars = struct.unpack('=8B',data_content[:8])
            for ch in num_chars:
                access_token += '%02x'%ch
            post_data = {'access_token':access_token,
                         'longtitude':obd_data[1],
						 'latitude':obd_data[2],
						 'DTC_CNT':obd_data[3],
						 'DTCFRZF':obd_data[4],
						 'LOAD_PCT':obd_data[5],
						 'ECT':obd_data[6],
						 'MAP':obd_data[7],
						 'RPM':obd_data[8],
						 'VSS':obd_data[9],
						 'SPARKADV':obd_data[10],
						 'IAT':obd_data[11],
						 'MAF':obd_data[12],
						 'TP':obd_data[13],
						 'RUNTM':obd_data[14],
						 'MIL_DIST':obd_data[15],
						 'FLI':obd_data[16],
						 'CLR_DIST':obd_data[17],
						 'VPWR':obd_data[18],
						 'AAT':obd_data[19],
						 'FUEL_TYP':obd_data[20],
                         'APP_R':obd_data[21]}
            post_data = json.dumps(post_data)
            res_data = call_http_api(url, post_data, 'post')
    elif pack_type == 255:
        print 'error message upload'
        url = ConfigAPI['base_url'] + 'vanet.obd.setErrorData'
        if pack_len == 11 :
            fmt = '=QB'
        else:
            fmt = '=QB'+str(pack_len-11)+'s'
        fmt_size = struct.calcsize(fmt)   # print fmt_size, len(data_content)
        if pack_len - 2 != len(data_content):
            pack_extras = 1
            res_data = response_json_error('packet struct invalid')
            logging.info(res_data)
        else:
            if pack_len == 11 :
                pid, error_type = struct.unpack(fmt, data_content)
                error_msg = ''
            else:
                pid,error_type,error_msg = struct.unpack(fmt, data_content)
            access_token = ''
            num_chars = struct.unpack('=8B',data_content[:8])
            for ch in num_chars:
                access_token += '%02x'%ch
            post_data = {'access_token':access_token,
						 'error_type': error_type,
						 'error_msg':error_msg,}
            post_data = json.dumps(post_data)
            res_data = call_http_api(url, post_data, 'post')
	# check reply message
	try:
		ret = json.loads(res_data)
	except:
		print 'json loads exception for res_data:', res_data
		ret['ret'] = 1
	
	print 'ret code: ', ret['ret']
	if ret['ret']!=0:	# if api failed, return a the message to client
		pack_extras = 1
	if (pack_extras == 1):
		if (stype == 'tcp'):
			client_socket.sendall("reply current time: " + time.ctime())
		else:	# udp
			send_bytes = client_socket.sendto(res_data, address)
			print 'send len: %d, fact len: %d' % (send_bytes, len(res_data))
			if (send_bytes != len(res_data)):
				err_msg = 'udp sendto fail, data length: %d, send_bytes: %d' % (len(res_data), send_bytes)
				raise gevent.socket.error


# tcp handler
def peer_tcp_handler(client_socket, address):
	# client socket config parameters
	# client socket config parameters
	timeout = 100
	
	# config the client socket
	client_socket.settimeout(timeout)
	while 1:
		try:
			# get packet length
			packet_len = client_socket.recv(2);	# length of message is 2 bytes
			print 'packet_len length: %d bytes' % len(packet_len)
			if (len(packet_len) < 2):
				err_msg = 'VANET: client msg of length error, recv length: %d' % len(packet_len)
				logging.error(err_msg)
				raise gevent.socket.error, err_msg
			length = struct.unpack('H', packet_len)[0]
			print 'length: %d' % length
			if (length < 4):
				err_msg = 'VANET: msg length of content error, content length: %d' % length
				logging.error(err_msg)
				raise gevent.socket.error, err_msg
			# get packet content
			packet_content = ''
			recv_len = length
			while recv_len > 0:
				print 'need recv_len: %d' % recv_len
				packet_content += client_socket.recv(recv_len)
				recv_len = length - len(packet_content)
			
			# build standard packet
			std_packet = packet_len + packet_content
			print std_packet
			# handle the packet
			packet_handler(client_socket, address, std_packet)
			
		except gevent.socket.error as msg:
			raise gevent.socket.error, msg;
		except:
			traceback.print_exc()
			raise gevent.socket.error, 'VANET: socket error'

if __name__ == '__main__':
	data = '\1\0\12\0\1'
	packet_handler('','',data)
	print 'data len: ', len(data)
	for ch in data:
		print struct.unpack('B',ch)

