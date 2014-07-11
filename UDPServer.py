#!/usr/bin/env python
# encoding: utf-8

# Copyright (c) 2013 liudanking
"""A simple UDP server.

For every message received, it sends a reply back.

You can use udp_client.py to send a message.
"""
from gevent.server import DatagramServer
from gevent.pool import Pool
from config import *
import vanet

# import log module
import log
import logging


class VANETDatagramServer(DatagramServer):
    def handle(self, data, address):
        print 'from %s: got %r' % (address[0], data)
        #self.sendto('reply: ' + data, address)
        vanet.packet_handler(self.socket, address, data, 'udp')


if __name__ == '__main__':
    try:
        pool = Pool(10000)
        udp_server = VANETDatagramServer((ConfigServer['udp_host'], ConfigServer['udp_port']), spawn=pool)
        print 'Receiving datagrams on %s:%s' % (ConfigServer['udp_host'], ConfigServer['udp_port'])
        udp_server.serve_forever()
        VANETDatagramServer((ConfigServer['udp_host'], ConfigServer['udp_port']), spawn=pool).serve_forever()
    except:
        print '###### server error ######'
        logging.info('server error')
