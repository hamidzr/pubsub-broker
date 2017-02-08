import zmq
from classes.event import *
from random import randint

# assumptions:
# 	only one topic per publisher
class Publisher:
	# attribiutes
	addr = randint(1000,9999)
	pId = randint(0,999)
	context = zmq.Context()
	socket = context.socket(zmq.PUSH)
	topic = 'unknown'
    # constructor
	def __init__(self, esAddr, strength ,topic):
		# self.data = []
		self.socket.connect("tcp://" + esAddr+ ":5555")
		self.topic = topic
		self.strength = strength

	def register(self):

		self.socket.send_string("rp{}-{}, {}, {}".format(self.pId, self.addr,self.topic,self.strength))

	
	def publish(self, event):
		self.socket.send_string("ev{}-{}".format(self.pId, event.serialize()))
		print('published: ' + event.serialize())