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
	print 'no arguments provided, resorting to defaults'
	eventserver_address = '127.0.0.1'
	owner_strength = 1
	topic = 'book'

logging.basicConfig(filename='publishLog.log',level=logging.DEBUG)

p1 = Publisher(eventserver_address,owner_strength,topic)
p1.register()
# keep publishing
while True:
	body = "body {}".format(randint(0,9))
	e1 = Event(p1.topic,body)
	p1.publish(e1)
	logging.info(e1.serialize())
	logging.info(str(datetime.datetime.now().time()))
	# sleep for 300ms
	time.sleep(2)
