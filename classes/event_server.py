import zmq
import collections
from classes.heartbeat_server import *
from classes.event import *
from classes.utils import *
import logging
import commands
import json
from random import randint
from classes.ringOrganizer import *
from uhashring import HashRing


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
	repSocket = context.socket(zmq.REP)
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
	def __init__(self,address):
		self.addr = address
		logger.info('EventServer addr: ' + address)
		self.repSocket.bind("tcp://"+address)
		self.pubSocket.bind("tcp://"+getPubFromAddress(address))
		self.mHashRing = HashRing(nodes=[address])
		self.mRingOrganizer = ringOrganizer(self.mHashRing, getRingOrgFromAddress(address))
		self.mRingOrganizer.nodes.add(address)

	# handles different message types
	# will return and event if the message is and event else will return false
	def detectMsgType(self):
		string = self.repSocket.recv()
		msg = json.loads(string)

		# check if message is a register req
		# dont forget to reply to the request
		if msg['msgType'] == 'publisherRegisterReq':
			self.handlePublisherRegistration(msg)
		elif msg['msgType'] == 'subscriberRegisterReq':
			self.handleSubscriberRegistration(msg)
		elif msg['msgType'] == 'nodeLookup':
			self.findRingNode(msg)
		elif msg['msgType'] == 'event':
			self.repSocket.send(b"ack")
			# check if it's a good source. check against a good 'set' of publishers
			if msg['pId'] in self.dominantPublishersSet:
				return self.getEvent(msg['eventDetails'])
			else:
				logger.info('discarded a weak event from ' + msg['pId'])
		else:
			logger.warning('unknown message type')
			self.repSocket.send(b"wrong message type ")

		return False

	def getEvent(self,event):
		return Event.deSerialize(event)

	def publish(self, event):
		# TODO make a publishable event method
		self.pubSocket.send_string("{} {} {}".format(event.topic, event.body, event.createdAt))
		logger.info('published: ' + event.__str__())

	def handlePublisherRegistration(self,msg):
		# currently handles publisher registration
		pId = msg['pId']
		logger.info('publisher registeration req received')
		toAppend =False #reminder for whether register this publisher
		# store the publisher in a publishers array for later use (if a publisher failed)
		publisher = self.publisher._make([pId,msg['address'],msg['topic'],msg['os']])
		self.publishers.append(publisher)

		if len(self.dominantPublishers)==0:
			toAppend=True
		for dp in self.dominantPublishers:
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

		#self.repSocket.send(b"registration ")
		suggestions = self.mRingOrganizer.suggestNodes()
		self.repSocket.send_string(suggestions)
		# self.store(self.getEvent(msg))
		# self.publish(self.getEvent(msg))

	def handleSubscriberRegistration(self,msg):
		logger.info('subscriber registeration req received')
		subscriber = self.subscriber._make([msg['sId'],msg['address'],msg['topic']])
		self.subscribers.append(subscriber)
		logger.info( 'list of all registered subscribers: ' + self.subscribers.__str__())
		self.repSocket.send(b"registred ")
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
		logger.info('unregistering publisher ' + publisher.__str__())
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
		
		return event # why returning event?

	def sendHistory(self, subscriber):
		# publish events from history based on a new subscriber.topic
		
		logger.info('sending history')
		if subscriber.topic in self.history :
			ls= list(self.history[subscriber.topic])
			for evnt in ls :
				self.publish(evnt)	
		else :
			logger.info ("no history found")		

	def findRingNode(self,msg):
		# TODO  determine the node that the subscriber or publisher should register to
		# return my address for now

		designatedEs = self.mRingOrganizer.hr.get_node(msg['key'])
		self.repSocket.send_string(designatedEs)


	def joinNotifyNode(self,neighborAddress):
		# add it to our own nodesTable
		self.mRingOrganizer.nodes.add(neighborAddress)
		self.mRingOrganizer.hr.add_node(neighborAddress)
		# notify the neighbor to add us to it's table
		msg = {'type': 'nodeJoinReq', 'address':self.addr}
		#connect to neighborRingOrganizer
		reqSocket = self.context.socket(zmq.REQ)
		reqSocket.connect("tcp://"+getRingOrgFromAddress(neighborAddress))
		reqSocket.send(json.dumps(msg))
		suggestedNodes = reqSocket.recv()
		reqSocket.disconnect("tcp://"+getRingOrgFromAddress(neighborAddress))
		# TODO make this recursive
		for nodeAddress in suggestedNodes.split(', '):
			# if I dont know this node
			if (nodeAddress not in self.mRingOrganizer.nodes):
				self.mRingOrganizer.nodes.add(nodeAddress)
				self.mRingOrganizer.hr.add_node(nodeAddress)
				reqSocket.connect("tcp://"+getRingOrgFromAddress(nodeAddress))
				reqSocket.send(json.dumps(msg))
				print('more suggestions: ', reqSocket.recv())
				reqSocket.disconnect("tcp://"+getRingOrgFromAddress(nodeAddress))

	def start(self):
		heartbeatServer(self).start()
		self.mRingOrganizer.start()
		logger.info('started')
		while True:
			# if the message is an event
			event = self.detectMsgType()
			if (event): 
				self.store(event)
				self.publish(event)
			
