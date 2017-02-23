from classes.publisher import *
from random import randint
import sys # to get cli args
import datetime
import logging
#create a publisher and pass in intial configuration

if len(sys.argv) == 4:
	# set the variables from the arguments passed	
	eventserver_address = sys.argv[1]
	topic = sys.argv[2]
	owner_strength = sys.argv[3]
else:
	logging.debug( 'no arguments provided, resorting to defaults')
	eventserver_address = '127.0.0.1:5555'
	owner_strength = 1
	topic = 'book'

p1 = Publisher(eventserver_address,owner_strength,topic)
srvAddr = p1.lookup(topic)
p1.register(srvAddr)
# keep publishing
while True:
	body = "{}".format(randint(0,9))
	e1 = Event(p1.topic,body)
	p1.publish(e1)
	# sleep for 2s
	time.sleep(2)
