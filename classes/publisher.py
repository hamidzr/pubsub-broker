import zmq
from classes.event import *
from classes.heartbeat_client import *
from random import randint
import logging

# assumptions:
# 	only one topic per publisher
class Publisher:
	# attribiutes
	addr = str(randint(10000,9999))
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
		# logging.basicConfig(filename="log/{}.log".format('P' + self.addr),level=logging.DEBUG)

	def register(self):
		heartbeatClient(self.pId,self.esAddr).start()
		self.socket.send_string("rp{}-{}, {}, {}".format(self.pId, self.addr,self.topic,self.strength))

	
	def publish(self, event):
		self.socket.send_string("ev{}-{}".format(self.pId, event.serialize()))
		print('published: ' + event.serialize())