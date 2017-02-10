from classes.publisher import *
from random import randint
import sys # to get cli args
import time

#create a publisher and pass in intial configuration

if len(sys.argv) == 4:
	# set the variables from the arguments passed	
	eventserver_address = sys.argv[1]
	topic = sys.argv[2]
	owner_strength = sys.argv[3]
else:
	logging.debug( 'no arguments provided, resorting to defaults')
	eventserver_address = '127.0.0.1'
	owner_strength = 1
	topic = 'book'

p1 = Publisher(eventserver_address,owner_strength,topic)
p1.register()
# keep publishing
while True:
	body = "body {}".format(randint(0,9))
	e1 = Event(p1.topic,body)
	p1.publish(e1)
	# sleep for 300ms
	time.sleep(2)
