from classes.subscriber import *
from classes.event import *
import sys # to get cli args
import datetime
import logging
if len(sys.argv) == 3:
	esAddr = sys.argv[1]
	topic = sys.argv[2]
else:
	print 'no arguments provided, resorting to defaults'
	esAddr = '127.0.0.1'
	topic = 'book'

#create a subscriber
s1 = Subscriber(esAddr)
# set the variables from the arguments passed
#subscribe to a topic
s1.register(topic)
s1.subscribe(topic)

logging.basicConfig(filename='subscribeLog.log',level=logging.DEBUG)

while True:
	event = Event.deSerialize(s1.socket.recv_string())
	logging.info(event.serialize())
	logging.info(str(datetime.datetime.now().time()))
	print('recieved: '+ event.topic)
