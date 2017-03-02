import zmq
from classes.event import *
from classes.heartbeat_client import *
from random import randint
import logging
import json

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
	pId = str(randint(0,999))
	context = zmq.Context()
	socket = context.socket(zmq.REQ)
	topic = 'unknown'
    # constructor
	def __init__(self, knownEsAddress, strength ,topic):
		# self.data = []
		self.knownEsAddress = knownEsAddress
		self.socket.connect("tcp://" + self.knownEsAddress)
		self.topic = topic
		self.strength = strength
		self.nodes = set([]) #suveni

	def register(self,serverAddress):
		self.socket.disconnect("tcp://" + self.knownEsAddress)
		self.socket.connect("tcp://" + serverAddress)
		heartbeatClient(self.pId,serverAddress,self).start() #suveni
		msg = {'msgType':'publisherRegisterReq','pId':self.pId,'address':self.addr, 'topic':self.topic,'os':self.strength}
		self.socket.send_string(json.dumps(msg))
		self.socket.recv()
		logger.info('register request sent')

	def lookup(self,key):
		msg = {'msgType':'nodeLookup', 'key': key}
		self.socket.send_string(json.dumps(msg))
		designatedServer = self.socket.recv()
		print('designated server:' , designatedServer)
		return designatedServer


	
	def publish(self, event):
		msg = {'msgType':'event','pId':self.pId,'eventDetails': {'topic':event.topic,'body':event.body,'createdAt':event.createdAt}}
		self.socket.send_string(json.dumps(msg))
		self.socket.recv()
		# self.socket.send_string("ev{}-{}".format(self.pId, event.serialize()))
		logger.info('published: ' + event.__str__())
