from classes.subscriber import *
from classes.event import *

#create a subscriber
s1 = Subscriber()

#subscribe to a topic
s1.subscribe("topic a")
while True:
	event = Event.deSerialize(s1.socket.recv_string())
	print('recieved: '+ event.topic)