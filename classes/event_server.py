import zmq
from classes.event import *
class EventServer:
	# attribiutes

	context = zmq.Context()
	pullSocket = context.socket(zmq.PULL)
	pubSocket = context.socket(zmq.PUB)
	history=[]
	publishers=[]
	# a set of current best publisher IDs
	dominantPublishers=[] # TODO generate a python set of dominant publisher IDs

	# constructor
	def __init__(self):
		self.pullSocket.bind("tcp://*:5555")
		self.pubSocket.bind("tcp://*:6666")

	def detectMsgType(self):
		string = self.pullSocket.recv()
		msgType = string[0]
		publisherId = string[1:].split('-')[0] # OPTIMIZE omg needs improving
		msg = string[1:].split('-')[1]

		# check if message is a register req
		if msgType == 'r':
			self.handleRegistration(publisherId,msg)
			return False
		else:
			# check if it's a good source. check against a good 'set' of publishers
			if True:
				return self.getEvent(msg)
			else:
				print('discarded a weak event')

	def getEvent(self,string):
		event = Event.deSerialize(string)
		print('received event: ', event.serialize());
		return event

	def publish(self, event):
		self.pubSocket.send_string(event.serialize())
		print('published: ' + event.serialize())

	def handleRegistration(self,pId,msg):
		# currently handles publisher registration
		msgArr = msg.split(', ')
		self.publishers.append({'pId': pId, 'addr':msgArr[0],'topic':msgArr[1], 'os':msgArr[2]})
		print 'publisher registred', pId, msg
		print 'current publishers array: ', self.publishers
		

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
