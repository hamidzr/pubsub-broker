from classes.publisher import *
from random import randint
import sys # to get cli args
import time

#create a publisher and pass in intial configuration

if len(sys.argv)<4:
	print 'pass ES_address, owner_strength and topic in this order as arguments'
	sys.exit(1)

# set the variables from the arguments passed	
eventserver_address = sys.argv[1]
owner_strength = sys.argv[2]
topic = sys.argv[3]

p1 = Publisher(eventserver_address,owner_strength,topic)
p1.register()
# keep publishing
while True:
	body = "body {}".format(randint(0,9))
	e1 = Event(p1.topic,body)
	p1.publish(e1)
	# sleep for 300ms
	time.sleep(2)
