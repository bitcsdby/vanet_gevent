# Copyright (c) 2013 liudanking
"""A simple UDP server.

For every message received, it sends a reply back.

You can use udp_client.py to send a message.
"""
from gevent.server import DatagramServer


class CarDatagramServer(DatagramServer):
    def handle(self, data, address):
		print '%s: got %r' % (address[0], data)
		self.sendto('reply: ' + data, address)


if __name__ == '__main__':
    print 'Receiving datagrams on :9000'
    CarDatagramServer(':9001').serve_forever()
