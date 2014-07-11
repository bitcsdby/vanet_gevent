#!/usr/bin/env python
# encoding: utf-8
"""Simple server that listens on port 6000 and echos back every input to the client.

Connect to it with:
  telnet localhost 6000

Terminate the connection by terminating telnet (typically Ctrl-] and then 'quit').
"""
from gevent.server import StreamServer
from gevent.pool import Pool
import gevent
import time
import vanet
from config import *

# import log module
import log
import logging
import SocketServer


# this handler will be run for each incoming connection in a dedicated greenlet
def handle(client_socket, address):
	print ('New connection from %s:%s' % address)
	try:
		vanet.peer_tcp_handler(client_socket, address)
	except gevent.socket.error as msg:
		print ('#### socket error: %s ####' % (msg))
		logging.info(msg)
	except Exception as e:
		for attr in dir(e):
			print attr + ':' + str(getattr(e,attr))
	except:
		print '########## UNKNOWN ERROR!!!! ########'
	finally:
		client_socket.shutdown(2)
		client_socket.close()
		print 'client socket %s:%s closed' % address
		



if __name__ == '__main__':
	pool = Pool(10000) # do not accept more than 10000 connections
	# to make the server use SSL, pass certfile and keyfile arguments to the constructor
	server = StreamServer((ConfigServer['tcp_host'], ConfigServer['tcp_port']), handle, spawn=pool)
	# to start the server asynchronously, use its start() method;
	# we use blocking serve_forever() here because we have no other jobs
	print ('Starting tcp server on %s:%s' % (ConfigServer['tcp_host'], ConfigServer['tcp_port']))
	try:
		server.serve_forever()
	except:
		print 'server error'
