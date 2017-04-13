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
	eventserver_address = '127.0.0.1'
	owner_strength = 1
	topic = 'book'

#logging.basicConfig(filename='publishLog.log',level=logging.DEBUG, mode='w')
#filehandler_dbg = logging.FileHandler(logger.name + '-debug.log', mode='w')

# logger = logging.getLogger('publishLog')
# hdlr = logging.FileHandler('publishLog.log',mode='w')
# logger.addHandler(hdlr) 
# logger.setLevel(logging.INFO)

p1 = Publisher(eventserver_address,owner_strength,topic)
p1.register()
# keep publishing
while True:
	body = "body {}".format(randint(0,9))
	e1 = Event(p1.topic,body)
	p1.publish(e1)
	# logger.info(e1.serialize())
	# logger.info(str(datetime.datetime.now().time()))
	# sleep for 2s
	time.sleep(2)
