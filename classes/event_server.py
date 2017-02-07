import zmq
import collections

from classes.event import *
class EventServer:
	# attribiutes

	context = zmq.Context()
	pullSocket = context.socket(zmq.PULL)
	pubSocket = context.socket(zmq.PUB)
	history={}  #History is a dictionary that mapping from topic name to deque
	
	publisher=collections.namedtuple('publisher', 'pId addr topic os') # TODO generate a python set of dominant publisher IDs
	dominantPublishers=[]
	# a set of current best publisher IDs, for better lookup performance
	dominantPublishersSet=set()
	publishers=[] # keep a log of all publishers for future use
	subscriber=collections.namedtuple('subscriber', 'sId addr topic') # TODO generate a python set of dominant publisher IDs
	subscribers=[]

	# constructor
	def __init__(self):
		self.pullSocket.bind("tcp://*:5555")
		self.pubSocket.bind("tcp://*:6666")

	def detectMsgType(self):
		string = self.pullSocket.recv()
		msgType = string[0:2]
		Id = string[2:].split('-')[0] # OPTIMIZE omg needs improving
		msg = string[2:].split('-')[1]

		# check if message is a register req
		if msgType == 'rp':
			self.handlePublisherRegistration(Id,msg)
			return False
		elif msgType == 'rs':
			self.handleSubscriberRegistration(Id,msg)
			return False			
		else:
			# check if it's a good source. check against a good 'set' of publishers
			# if you reach here it must be an event from a publisher
			if Id in self.dominantPublishersSet:
				self.store(self.getEvent(msg))
			else:
				print('discarded a weak event')

	def getEvent(self,string):
		event = Event.deSerialize(string)
		#try not to print here
		#print('received event: ', event.serialize());
		
		
		
		return event

	def publish(self, event):
		self.pubSocket.send_string(event.serialize())
		print('published: ' + event.serialize())

	def handlePublisherRegistration(self,pId,msg):
		# currently handles publisher registration
		msgArr = msg.split(', ')
		#self.publishers.append({'pId': pId, 'addr':msgArr[0],'topic':msgArr[1], 'os':msgArr[2]})
		toAppend =False #reminder for whether register this publisher
		print '!!!!!!!!!!!!! Entered the function'
		# store the publisher in a publishers array for later use (if a publisher failed)
		self.publishers.append(self.publisher._make([pId,msgArr[0],msgArr[1],msgArr[2]]))
		if len(self.dominantPublishers)==0:
			toAppend=True
			print '!!!!!!!!!!!!! Nothing in the dps'	
		for dp in self.dominantPublishers:
			print '!!!!!!!!!!!!! Entered the loop'
			if dp.topic is msgArr[1]:  #found the publisher with same topic
				if dp.os<msgArr[2]: #remove every publisher with lower os
					self.dominantPublishers.remove(dp)
					self.dominantPublishersSet.remove(dp.pId)
					toAppend=True
				# dont keep a publisher with same OS,
				# elif dp.os==msgArr[2]: #when the two have same os, keep them both
				# 	toAppend=True
				else:
					break 	#dont do anything since there is already a publisher with higher os
			else:
				toAppend=True #since no publisher found, register this new publisher 
		if toAppend:	#check if need to register this publisher
			print '!!!!!!!!!!!!! Im gonna append'			
			self.dominantPublishers.append(self.publisher._make([pId,msgArr[0],msgArr[1],msgArr[2]]))
			self.dominantPublishersSet.add(pId)
		
		print 'Number of elem in PDS', len(self.dominantPublishers)
		print 'publisher registr request', pId, msg
		print 'current dominantpublishers array: '
		for p in self.dominantPublishers:
			print 'pId %s , address %s , topic %s , strength %s' % p
		print 'current dominant publishers: ',self.dominantPublishers
		print 'current dominant publishers set: ',self.dominantPublishersSet
		print 'list of all registered publishers: ',self.publishers

		self.store(self.getEvent(msg))

	def handleSubscriberRegistration(self,sId,msg):
		pass

	def store(self,event):
		if event.topic in self.history:
			if len(self.history[event.topic]) <=10 :
				print 'Entered '
				self.history[event.topic].append(event)
			else :
				self.history[event.topic].popleft()
				self.history[event.topic].append(event)
		else :
			queue=collections.deque([event])
			self.history[event.topic]=queue
		print 'number of history message ', len(self.history[event.topic])
		for evnt in self.history[event.topic] :
			self.publish(evnt)
		
		return event

	def start(self):
		# multithreaded??
		while True:
			# if the message is an event
			self.detectMsgType()
			# TODO we dont want to put everythin in detectMsgType()
			
