from classes.subscriber import *

s1 = Subscriber()
s1.subscribe("topic a")
while True:
	string = s1.socket.recv_string()
	print('recieved: ' + string)