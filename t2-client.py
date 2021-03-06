import socket
import sys
import time

HOST, PORT = "localhost", 9000
data = 'data from client'

# SOCK_DGRAM is the socket type to use for UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# As you can see, there is no connect() call; UDP has no connections.
# Instead, data is directly sent to the recipient via sendto().
while True:
	sock.sendto(data + "\n", (HOST, PORT))
	received = sock.recv(1024)
	print "Sent:     {}".format(data)
	print "Received: {}".format(received)
	time.sleep(1)