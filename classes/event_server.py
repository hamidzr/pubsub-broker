import zmq
import collections
from classes.heartbeat_server import *
from classes.event import *
import logging
from random import randint
import commands

logging.basicConfig(level=logging.INFO)
# logging.basicConfig(filename="log/{}.log".format('ES' + self.addr),level=logger.info)
logger = logging.getLogger(__name__) #Q will this make it shared between all objects?
hdlr = logging.FileHandler('eventServer.log',mode='w')
logger.addHandler(hdlr)

class EventServer:
	# attribiutes
	
	# current host's ip address
	addr = str(randint(1000,9999))
	# addr = commands.getstatusoutput("ifconfig | awk '/inet addr/{print substr($2,6)}' | sed -n '1p'")[1]
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


	# handles different message types
	# will return and even if the message is and event else will return false
	def detectMsgType(self):
		string = self.pullSocket.recv()
		msgType = string[0:2]
		Id = string[2:].split('-')[0] # OPTIMIZE omg needs improving
		msg = string[2:].split('-')[1]

		# check if message is a register req
		if msgType == 'rp':
			logger.info('publisher registeration req received')
			self.handlePublisherRegistration(Id,msg)
			return False
		elif msgType == 'rs':
			self.handleSubscriberRegistration(Id,msg)
			return False			
		else:
			# check if it's a good source. check against a good 'set' of publishers
			# if you reach here it must be an event from a publisher
			if Id in self.dominantPublishersSet:
				return self.getEvent(msg)
			else:
				logger.info('discarded a weak event')
				return False

	def getEvent(self,string):
		event = Event.deSerialize(string)
		#try not to print here
		#print('received event: ', event.serialize());
		return event

	def publish(self, event):
		self.pubSocket.send_string(event.serialize())
		logger.info('published: ' + event.serialize())

	def handlePublisherRegistration(self,pId,msg):
		# currently handles publisher registration
		msgArr = msg.split(', ')
		#self.publishers.append({'pId': pId, 'addr':msgArr[0],'topic':msgArr[1], 'os':msgArr[2]})
		toAppend =False #reminder for whether register this publisher
		# store the publisher in a publishers array for later use (if a publisher failed)
		publisher = self.publisher._make([pId,msgArr[0],msgArr[1],msgArr[2]])
		self.publishers.append(publisher)

		if len(self.dominantPublishers)==0:
			toAppend=True
			#print '!!!!!!!!!!!!! Nothing in the dps'
		for dp in self.dominantPublishers:
			#print '!!!!!!!!!!!!! Entered the loop'
			if dp.topic == publisher.topic:  #found the publisher with same topic
				if dp.os < publisher.os: #remove every publisher with lower os
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
			self.dominantPublishers.append(publisher)
			self.dominantPublishersSet.add(pId)

		self.store(self.getEvent(msg))
		self.publish(self.getEvent(msg))

	def handleSubscriberRegistration(self,sId,msg):
		logger.info( msg)
		msgArr = msg.split(', ')
		addr = msgArr[0]
		topic = msgArr[1]
		subscriber = self.subscriber._make([sId,addr,topic])
		self.subscribers.append(subscriber)
		logger.info( 'list of all registered subscribers: ',self.subscribers)
		self.sendHistory(subscriber)


	def unregisterPublisher(self, pId):
		#grab the publisher
		publisher = ''
		for pub in self.publishers:
			if pub.pId == pId:
				publisher = pub
				break;
			else:
				return False;
		self.publishers.remove(publisher)
		# if it was a dominantPublisher we need to do more stuff
		if publisher.pId in self.dominantPublishersSet:
			self.dominantPublishers.remove(publisher)
			self.dominantPublishersSet.remove(publisher.pId)
			self.calcDominantPublisher(publisher.topic)
		logger.info( self.dominantPublishersSet)


	def calcDominantPublisher(self,topic):
		dominantPublisher = self.publisher._make([127,'addr',topic,-1])
		for pub in self.publishers:
			if pub.topic == topic and pub.os > dominantPublisher.os:
				dominantPublisher = pub
		logger.info( 'new dominantPublisher to add is ')
		logger.info( dominantPublisher)
		self.dominantPublishers.append(dominantPublisher)
		self.dominantPublishersSet.add(dominantPublisher.pId)

	def store(self,event):
		if event.topic in self.history:
			if len(self.history[event.topic]) <=10 :
				self.history[event.topic].append(event)
			else :
				self.history[event.topic].popleft()
				self.history[event.topic].append(event)
		else :
			queue=collections.deque([event])
			self.history[event.topic]=queue
		#for evnt in self.history[event.topic] :
		#	self.publish(evnt)
		
		return event

	def sendHistory(self, subscriber):
		# publish events from history based on a new subscriber.topic
		
		logger.info('sending history')
		if subscriber.topic in self.history :
			ls= list(self.history[subscriber.topic])
			for evnt in ls :
				self.publish(evnt)	
		else :
			logger.info ("no history found")		

	def findRingNode():
		# TODO  determine the node that the subscriber or publisher should register to
		# return my address for now
		pass

	def start(self):
		heartbeatServer(self).start()
		logger.info('started')
		while True:
			# if the message is an event
			event = self.detectMsgType()
			if (event): 
				self.store(event)
				self.publish(event)
			
