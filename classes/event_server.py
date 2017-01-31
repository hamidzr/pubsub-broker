import zmq
from classes.event import *
class EventServer:
	# attribiutes

	context = zmq.Context()
	pullSocket = context.socket(zmq.PULL)
	pubSocket = context.socket(zmq.PUB)
	history=[]
	publishers={}

	# constructor
	def __init__(self):
		self.pullSocket.bind("tcp://*:5555")
		self.pubSocket.bind("tcp://*:6666")

	def detectMsgType(self):
		msg = self.pullSocket.recv()
		if msg.startswith('register'):
			self.register(msg)
			return False
		else:
			# check if it's a good source
			msgArr = msg.split('-')
			return self.getEvent(msgArr[1])

	def getEvent(self,string):
		event = Event.deSerialize(string)
		# redundant serialization
		print('received event: ', event.serialize());
		return event

	def publish(self, event):
		self.pubSocket.send_string(event.serialize())
		print('published: ' + event.serialize())

	def register(self,msg):
		# QUESTION  how to detect who is sending?
		print 'registration req received', msg

	def store(self,event):
		self.history.append(event)

	def start(self):
		# multithreaded??
		while True:
			# if the message is an event
			event = self.detectMsgType()
			if event:
				# event = self.getEvent()
				self.store(event)
				self.publish(event)
