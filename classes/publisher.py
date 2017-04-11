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
		#self.socket.connect("tcp://" + self.knownEsAddress)
		self.topic = topic
		self.strength = strength
#QUESTION--shouldn't this heartBeatClient connect to the suggested node?
		#self.heartBeatClientObject=heartbeatClient(self.pId,knownEsAddress)
		#self.heartBeatClientObject=heartbeatClient(self.pId,knownEsAddress,self)#suveni
		#self.heartBeatClientObject.start()
		self.nodes=set([])
		self.serverAddress= knownEsAddress

	def register(self,serverAddress):
		self.socket.disconnect("tcp://" + self.knownEsAddress)
		self.socket.setsockopt(zmq.RCVTIMEO, 1000)
		#Check before Register
		try:
			self.socket.connect("tcp://" + serverAddress)
			#self.heartBeatClientObject.start()
			msg = {'msgType':'publisherRegisterReq','pId':self.pId,'address':self.addr, 'topic':self.topic,'os':self.strength}
			self.socket.send_string(json.dumps(msg))
			nodesReceived=self.socket.recv()
			for nodeAddress in nodesReceived.split(', '):
				# if I dont know this node
				print("I received!!!!!")
				if (nodeAddress not in self.nodes):
					#store the ip of this node
					self.nodes.add(nodeAddress)
			# self.socket.send_string("rp{}-{}, {}, {}".format(self.pId, self.addr,self.topic,self.strength))
			logger.info('register request sent')
			self.heartBeatClientObject = heartbeatClient(self.pId, serverAddress, self)  # suveni
			self.heartBeatClientObject.start()


			return True
		except:
			print ("The node where about to register is dead")
			self.socket.disconnect("tcp://" + self.serverAddress)
			self.resetSocket()
			self.notifyOthers(self.serverAddress)

			#delete the node locally
			for nodeAddress in self.nodes.copy():
				if nodeAddress == serverAddress:
					#store the ip of this node
					self.nodes.remove(nodeAddress)
					break



			return False
			#TRY TO RE-LOOKUP
			#NOt Finished

	def lookup(self,key):
		if self.nodes:
			self.knownEsAddress=next(iter(self.nodes))
		self.socket.connect("tcp://" + self.knownEsAddress)
		msg = {'msgType':'nodeLookup', 'key': key}
		self.socket.send_string(json.dumps(msg))
		designatedServer = self.socket.recv()
		self.serverAddress=designatedServer
		print('designated server:' , designatedServer)
		result= self.register(designatedServer)


		#self.register(designatedServer)
		return result
		# TODO go register to the designate

	def notifyOthers(self, deadNodeAddr):
		msg = {'type': 'nodeDeleteReq', 'address': deadNodeAddr}
		reqSocket = self.context.socket(zmq.REQ)
		for nodeAddress in self.nodes:
			# if I dont know this node
			if (nodeAddress != deadNodeAddr):
				reqSocket.connect("tcp://" + getRingOrgFromAddress(nodeAddress))
				reqSocket.send(json.dumps(msg))
				print(reqSocket.recv())
				reqSocket.disconnect("tcp://" + getRingOrgFromAddress(nodeAddress))

	def resetSocket(self):
		self.socket.close()
		self.socket = self.context.socket(zmq.REQ)
		self.socket.setsockopt(zmq.RCVTIMEO, 1000)  # milliseconds

	def publish(self, event):
		try:
			msg = {'msgType':'event','pId':self.pId,'eventDetails': {'topic':event.topic,'body':event.body,'createdAt':event.createdAt}}
			self.socket.send_string(json.dumps(msg))
			self.socket.recv()
			# self.socket.send_string("ev{}-{}".format(self.pId, event.serialize()))
			logger.info('published: ' + event.__str__())
			return True
		except:
			print ("the event server is dead !")
			#Notify other event servers
			self.notifyOthers(self.serverAddress)
			#reset socket
			self.socket.disconnect("tcp://" + self.serverAddress)
			self.resetSocket()

			#delete the node locally
			for nodeAddress in self.nodes.copy():
				if nodeAddress == self.serverAddress:
					#store the ip of this node
					self.nodes.remove(nodeAddress)
					break

			return False