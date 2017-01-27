import zmq
from classes.event import *

class Publisher:
	# attribiutes
	# id

    # constructor
    def __init__(self):
    	# self.data = []
	    context = zmq.Context()
	    socket = context.socket(zmq.PUB)
		socket.bind("tcp://*:5556")

    def publish(self, event):
		socket.send_string(event.toString())