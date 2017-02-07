from classes.subscriber import *
from classes.event import *
import sys # to get cli args

#create a subscriber
s1 = Subscriber()
# set the variables from the arguments passed	
topic = sys.argv[1]
#subscribe to a topic
s1.subscribe(topic)
while True:
	event = Event.deSerialize(s1.socket.recv_string())
	print('recieved: '+ event.topic)