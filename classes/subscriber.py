import json
import zmq
from random import randint
from classes.heartbeat_subscriber import *
import logging
from classes.utils import *
from classes.heartbeat_client import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) #Q will this make it shared between all objects?
hdlr = logging.FileHandler('subscriber.log',mode='w')
logger.addHandler(hdlr)

class Subscriber:
	# attribiutes
	sId = randint(0,999)
	addr = str(randint(1000,9999))+':'+str(randint(1000,9999))
	# addr = commands.getstatusoutput("ifconfig | awk '/inet addr/{print substr($2,6)}' | sed -n '1p'")[1]
	context = zmq.Context()
	subsocket = context.socket(zmq.SUB)
	#subsocket.bind("tcp://" + getPubFromAddress(addr))
	reqSocket = context.socket(zmq.REQ)

	
	# constructor
	def __init__(self,esAddr = "127.0.0.1:5555",topic= 'book'):
		# self.data = []
		self.knownEsAddress = esAddr
		self.topic=topic
		self.subsocket.connect("tcp://" + getPubFromAddress(self.knownEsAddress))
		self.reqSocket.setsockopt(zmq.RCVTIMEO, 1000)
		self.reqSocket.connect("tcp://" + self.knownEsAddress)
		self.nodes = set([])#suveni
		# logging.basicConfig(filename="log/{}.log".format('S' + self.addr),level=logging.DEBUG)
	
	def register(self,topic, serverAddress):
		self.resetSocket()
		self.reqSocket.connect("tcp://" + serverAddress)
		print("knownEsAddress: "+ self.knownEsAddress)
		print("serverAddress: " + serverAddress)
		if self.checkEventServer():
			#self.subsocket.disconnect("tcp://" + getPubFromAddress(self.knownEsAddress))
			self.subsocket.connect("tcp://" + getPubFromAddress(serverAddress))
			#heartbeatClient(self.sId,serverAddress,self).start()#suveni
			msg = {'msgType':'subscriberRegisterReq','sId':self.sId,'address':self.addr, 'topic':topic}
			self.reqSocket.send_string(json.dumps(msg))
			self.reqSocket.recv()
			logger.info( 'register req sent')
			self.subsocket.connect("tcp://" + getPubFromAddress(self.addr))
			print('subsocket connects to: '+getPubFromAddress(self.addr))
			print('subsocket connects to: ' + getPubFromAddress(serverAddress))
			self.heartBeatPublisherObject = heartbeatSubscriber(self.sId, serverAddress, self)  # suveni
			self.heartBeatPublisherObject.start()


			return True
		else:
			self.resetSocket()
			return False
	def lookup(self,key):
		if self.nodes:
			self.knownEsAddress=next(iter(self.nodes))
		self.reqSocket.connect("tcp://" + self.knownEsAddress)
		msg = {'msgType':'nodeLookup', 'key': key}
		self.reqSocket.send_string(json.dumps(msg))
		designatedServer = self.reqSocket.recv()
		print('designated server:' , designatedServer)
		return designatedServer

	def resetSocket(self):
		self.reqSocket.close()
		self.reqSocket = self.context.socket(zmq.REQ)
		self.reqSocket.setsockopt(zmq.RCVTIMEO, 100)  # milliseconds

	def subscribe(self, sFilter):
		# any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
		# system what it is interested in
		self.subsocket.setsockopt_string(zmq.SUBSCRIBE, sFilter.decode('ascii'))

		logger.info('subscription request to topic {} sent'.format(sFilter).decode('ascii'))

	def checkEventServer(self):
		try:
			msg = {'msgType': 'CheckCheck'}
			self.reqSocket.send_string(json.dumps(msg))

			nodesReceived = self.reqSocket.recv()
			for nodeAddress in nodesReceived.split(', '):
				# if I dont know this node
				if (nodeAddress not in self.nodes):
					# store the ip of this node
					self.nodes.add(nodeAddress)

			logger.info('Event Server is alive')
			return True
		except:
			print ("the event server is dead !")
			# delete the node locally
			for nodeAddress in self.nodes.copy():
				if nodeAddress == self.knownEsAddress:
					# store the ip of this node
					self.nodes.remove(nodeAddress)
					break

			return False