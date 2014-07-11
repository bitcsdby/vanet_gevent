#!/usr/bin/env python
# encoding: utf-8
"""Simple server that listens on port 6000 and echos back every input to the client.

Connect to it with:
  telnet localhost 6000

Terminate the connection by terminating telnet (typically Ctrl-] and then 'quit').
"""
from gevent.server import StreamServer
import gevent
import time

# import log module
import log
import logging


# TCP server here is used for small but frequent data transfer, so buffer size of 1024 is enough
bufferSize = 1024
client_count = 0
# this handler will be run for each incoming connection in a dedicated greenlet
def handle(socket, address):
	#client_count += 1
	#print type(socket)
	print ('New connection from %s:%s' % address)
	#print client_count
	while True:
		try:
			line = socket.recv(bufferSize)
			print 'received: ', line
			socket.sendall('reply: '+ line + "\ncurrent time: " + time.ctime())
			print 'echo: ', line
		except gevent.socket.error as msg:
			print '#### error: socket error ####';
			socket.close()
			break
		except:
			print '########## UNKNOWN ERROR!!!! ########'
			socket.close()
			break;

if __name__ == '__main__':
	# to make the server use SSL, pass certfile and keyfile arguments to the constructor
	server = StreamServer(('0.0.0.0', 6000), handle)
	# to start the server asynchronously, use its start() method;
	# we use blocking serve_forever() here because we have no other jobs
	print ('Starting echo server on port 6000')
	server.serve_forever()
