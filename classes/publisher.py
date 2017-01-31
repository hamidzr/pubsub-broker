import zmq
from classes.event import *
from random import randint

class Publisher:
	# attribiutes
	ip = randint(0,10000)
	context = zmq.Context()
	socket = context.socket(zmq.PUSH)
    # constructor
	def __init__(self, esAddr = '127.0.0.1:5555',strength = 1):
		# self.data = []
		self.socket.connect("tcp://" + esAddr)
		self.strength = strength

	def register(self):
		self.socket.send_string("register-publisher-ip:myIp-strength:{}-ip:{}".format(self.strength,self.ip))

	
	def publish(self, event):
		self.socket.send_string("{}-{}".format(self.ip, event.serialize()))
		print('published: ' + event.serialize())