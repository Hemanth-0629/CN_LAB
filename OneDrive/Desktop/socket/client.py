import socket # for socket
import sys

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	print ("Socket successfully created")
except socket.error as err:
	print ("socket creation failed with error %s" %(err))

port = 8000

try:
	host_ip = '127.0.0.1'
except socket.gaierror:
	print ("there was an error resolving the host")
	sys.exit()

s.connect((host_ip, port))

print ("the socket has successfully connected")
connected = True
while connected:
	msg = input("->")
	s.send(msg.encode('utf-8'))
	if(msg=="!DISCONNECT"):
		connected=False
	else:
		msg = s.recv(1024).decode('utf-8')
		print(f"Message from server: {msg}")
