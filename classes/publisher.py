import zmq
from classes.event import *

class Publisher:
	# attribiutes
	# id
	context = zmq.Context()
	socket = context.socket(zmq.PUB)
    # constructor
	def __init__(self):
		# self.data = []
		self.socket.bind("tcp://*:5555")
	
	def publish(self, event):
		self.socket.send_string(event.toString())
		print('published: ' + event.toString())