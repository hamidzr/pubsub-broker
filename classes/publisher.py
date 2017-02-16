import zmq
from classes.event import *
from classes.heartbeat_client import *
from random import randint
import logging

# assumptions:
# 	only one topic per publisher
# 	
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) #Q will this make it shared between all objects?
hdlr = logging.FileHandler('publisher.log',mode='w')
logger.addHandler(hdlr)

class Publisher:
	# attribiutes
	addr = str(randint(1000,9999))
	# addr = commands.getstatusoutput("ifconfig | awk '/inet addr/{print substr($2,6)}' | sed -n '1p'")[1]
	pId = randint(0,999)
	context = zmq.Context()
	socket = context.socket(zmq.PUSH)
	topic = 'unknown'
    # constructor
	def __init__(self, esAddr, strength ,topic):
		# self.data = []
		self.esAddr = esAddr
		self.socket.connect("tcp://" + esAddr+ ":5555")
		self.topic = topic
		self.strength = strength

	def register(self):
		# TODO address = lookup(self.topic)
		heartbeatClient(self.pId,self.esAddr).start()
		self.socket.send_string("rp{}-{}, {}, {}".format(self.pId, self.addr,self.topic,self.strength))
		logger.info('register request sent')

	def lookup(self,key):
		# TODO call to any known eventservice to findout where it should register.
		# return: ES address (ip:port)
		pass
	
	def publish(self, event):
		self.socket.send_string("ev{}-{}".format(self.pId, event.serialize()))
		logger.info('published: ' + event.serialize())
