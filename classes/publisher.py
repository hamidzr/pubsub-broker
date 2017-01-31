import zmq
from classes.event import *

class Publisher:
	# attribiutes
	# id
	context = zmq.Context()
	socket = context.socket(zmq.PUSH)
    # constructor
	def __init__(self, esAddr = '127.0.0.1:5555',strength = 1):
		# self.data = []
		self.socket.connect("tcp://" + esAddr)
		self.strength = strength
	
	def publish(self, event):
		self.socket.send_string(event.serialize())
		print('published: ' + event.serialize())