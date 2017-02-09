from classes.publisher import *
from classes.heartbeat_client import *
from random import randint
import sys # to get cli args
import time

#create a publisher and pass in intial configuration

if len(sys.argv) == 4:
	# set the variables from the arguments passed	
	eventserver_address = sys.argv[1]
	owner_strength = sys.argv[2]
	topic = sys.argv[3]
else:
	print 'no arguments provided, resorting to defaults'
	eventserver_address = '127.0.0.1'
	owner_strength = 1
	topic = 'book'

p1 = Publisher(eventserver_address,owner_strength,topic)
heartbeat_client = heartbeatClient(p1.pId,p1.esAddr)
p1.register()
# keep publishing
while True:
	body = "body {}".format(randint(0,9))
	e1 = Event(p1.topic,body)
	p1.publish(e1)
	# sleep for 300ms
	time.sleep(2)
