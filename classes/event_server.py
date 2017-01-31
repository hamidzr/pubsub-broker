import zmq
from classes.event import *
class EventServer:
	# attribiutes

	context = zmq.Context()
	pullSocket = context.socket(zmq.PULL)
	pubSocket = context.socket(zmq.PUB)
	history=[]

	# constructor
	def __init__(self):
		self.pullSocket.bind("tcp://*:5555")
		self.pubSocket.bind("tcp://*:6666")
	def getEvent(self):
		event = Event.deSerialize(self.pullSocket.recv())
		# redundant serialization
		print('received: ', event.serialize());
		return event

	def publish(self, event):
		self.pubSocket.send_string(event.serialize())
		print('published: ' + event.serialize())

	def store(self,event):
		dict[event.topic]=event.body;
		self.history.append(event)

	def start(self):
		# multithreaded??
		while True:
			event = self.getEvent()
			self.publish(event)
