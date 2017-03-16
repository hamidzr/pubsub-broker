from classes.subscriber import *
from classes.event import *
import sys # to get cli args
import datetime
import logging
import json
if len(sys.argv) == 3:
	esAddr = sys.argv[1]
	topic = sys.argv[2]
else:
	logging.debug( 'no arguments provided, resorting to defaults')
	esAddr = '127.0.0.1:5555'
	topic = 'book'

#create a subscriber
s1 = Subscriber(esAddr,topic)
# set the variables from the arguments passed
#subscribe to a topic
srvAddress = s1.lookup(topic)
registered=s1.register(topic, srvAddress)#subcorrect
while not registered:
	srvAddress = s1.lookup(topic)
	registered = s1.register(topic, srvAddress)  # subcorrect
	time.sleep(2)
s1.subscribe(topic)


logger = logging.getLogger('subscribeLog')
hdlr = logging.FileHandler('subscribeLog.log',mode='w')
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

while True:
	msg = s1.subsocket.recv()

	logger.info('recieved: ' + msg)
	#print('msg after split: ')
	#print(msg.split(' '))
	# if msg.split(' ')[1] == '-1':
	# 	print('I received ES is dead')
	# 	srvAddress = s1.lookup(topic)
	# 	alive = s1.register(topic, srvAddress)
	# 	s1.subscribe(topic)


