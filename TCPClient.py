import time
import socket
import struct

def myfunction(host, port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((host, port))
	finally:	
		while True:
			data = 'socket data'
			data_len = len(data)
			data_len = struct.pack('H',data_len)
			#s.sendall(data_len+data)
			s.sendall(data_len+data[:2])
			time.sleep(5)
			s.sendall(data[2:])
			print 'data send: ', data
			received = s.recv(1024)
			print 'data received: ', received
			time.sleep(1)
			
if __name__ == '__main__':
	#host = 'www.itec2014.com'
	host = '192.168.2.120'
	myfunction(host, 6000)