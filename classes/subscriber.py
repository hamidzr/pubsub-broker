import json
import zmq
from random import randint
import logging
from classes.utils import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) #Q will this make it shared between all objects?
hdlr = logging.FileHandler('subscriber.log',mode='w')
logger.addHandler(hdlr)

class Subscriber:
	# attribiutes
	sId = randint(0,999)
	addr = str(randint(1000,9999))
	# addr = commands.getstatusoutput("ifconfig | awk '/inet addr/{print substr($2,6)}' | sed -n '1p'")[1]
	context = zmq.Context()
	socket = context.socket(zmq.SUB)
	reqSocket = context.socket(zmq.REQ)

	
	# constructor
	def __init__(self,esAddr = "127.0.0.1:5555"):
		# self.data = []
		self.knownEsAddress = esAddr
		self.socket.connect("tcp://" + getPubFromAddress(esAddr))
		self.reqSocket.connect("tcp://" + esAddr)
		# logging.basicConfig(filename="log/{}.log".format('S' + self.addr),level=logging.DEBUG)
	
	def register(self,topic, serverAddress):
		self.socket.disconnect("tcp://" + getPubFromAddress(self.knownEsAddress))
		self.socket.connect("tcp://" + getPubFromAddress(serverAddress))
		msg = {'msgType':'subscriberRegisterReq','sId':self.sId,'address':self.addr, 'topic':topic}
		self.reqSocket.send_string(json.dumps(msg))
		self.reqSocket.recv()
		logger.info( 'register req sent')

	def lookup(self,key):
		msg = {'msgType':'nodeLookup', 'key': key}
		self.reqSocket.send_string(json.dumps(msg))
		designatedServer = self.reqSocket.recv()
		print('designated server:' , designatedServer)
		return designatedServer

	def subscribe(self, sFilter):
		# any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
		# system what it is interested in
		self.socket.setsockopt_string(zmq.SUBSCRIBE, sFilter.decode('ascii'))
		logger.info('subscription request to topic {} sent'.format(sFilter).decode('ascii'))