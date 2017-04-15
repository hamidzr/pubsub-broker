from classes.subscriber import *
from classes.event import *
import sys # to get cli args
import datetime
import logging
if len(sys.argv) == 2:
	topic = sys.argv[1]
else:
	print('bad arg')
	sys.exit()
#create a subscriber
s1 = Subscriber()
# set the variables from the arguments passed
#subscribe to a topic
leader_node = getLeadingEs(s1.zk)
leader_data = getNodeData(s1.zk,leader_node)
@s1.zk.DataWatch(leader_node)
def my_func(data,stat):
	leader = getLeadingEs(s1.zk)
	print("new leader is",getNodeData(s1.zk,leader))
	s1.register(getNodeData(s1.zk,leader)['addr'],topic)
	s1.subscribe(topic)	



logger = logging.getLogger('subscribeLog')
hdlr = logging.FileHandler('subscribeLog.log',mode='w')
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

while True:
	event = Event.deSerialize(s1.socket.recv_string())
	logger.info(event.serialize())

