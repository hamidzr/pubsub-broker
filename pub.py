from classes.publisher import *
from random import randint
import sys # to get cli args
import datetime
import logging
#create a publisher and pass in intial configuration
logger = logging.getLogger('publisherInstance')

if len(sys.argv) == 4:
	# set the variables from the arguments passed	
	topic = sys.argv[1]
	owner_strength = sys.argv[2]
else:
	logging.debug( 'no arguments provided, resorting to defaults')
	owner_strength = 5
	topic = 'book'

#logging.basicConfig(filename='publishLog.log',level=logging.DEBUG, mode='w')
#filehandler_dbg = logging.FileHandler(logger.name + '-debug.log', mode='w')

# logger = logging.getLogger('publishLog')
# hdlr = logging.FileHandler('publishLog.log',mode='w')
# logger.addHandler(hdlr) 
# logger.setLevel(logging.INFO)

p1 = Publisher(owner_strength,topic) 
leader_node = getLeadingEs(p1.zk)
leader_data = getNodeData(p1.zk,leader_node)
# p1.register(leader_data['addr'])
# watchLeader(p1.zk,leader_node,p1.register(),leader_data['addr'])
@p1.zk.DataWatch(leader_node)
def my_func(data,stat):
	leader = getLeadingEs(p1.zk)
	print("new leader is",getNodeData(p1.zk,leader))
	p1.register(getNodeData(p1.zk,leader)['addr'])

# keep publishing
while True:
	body = "body {}".format(randint(0,9))
	e1 = Event(p1.topic,body)
	p1.publish(e1)
	# logger.info(e1.serialize())
	# logger.info(str(datetime.datetime.now().time()))
	# sleep for 2s
	time.sleep(2)
