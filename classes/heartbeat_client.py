import zmq
import threading
import time
import logging
import sys
from classes.utils import *
import json


class heartbeatClient (threading.Thread):

	daemon = True # make it a deamon

	#def __init__(self, pId, servAddr):
	def __init__(self, pId, servAddr,pubSub):#suveni
		threading.Thread.__init__(self)
		self.pId = pId
		self.servAddr = servAddr
		context = zmq.Context()
		self.socket = context.socket(zmq.REQ)
		self.socket.connect("tcp://" + getHbServerFromAddress(servAddr))
		self.pubSub=pubSub#suveni

	#def changeServAddr(self,servAddr):
	#	self.socket.disconnect("tcp://" + getHbServerFromAddress(self.servAddr))
	#	self.socket.close()
	#	self.socket = self.context.socket(zmq.REQ)
	#	#HeartbeatClient keeps sending message to HeartbeatServer without caring about the timeout
	#	#self.socket.setsockopt(zmq.RCVTIMEO, 1000)
	#	self.servAddr=servAddr
	#	self.socket.connectself.socket.connect("tcp://" + getHbServerFromAddress(self.servAddr))

	def run(self):
		logging.basicConfig(level=logging.INFO)
		logger = logging.getLogger(__name__)  # Q will this make it shared between all objects?
		hdlr = logging.FileHandler('heartbeatClient.log', mode='w')
		logger.addHandler(hdlr)

		logger.info('we are alive - heartbeating')
		while True:
			try:
				self.socket.send(b"{}".format(self.pId))
				ack = self.socket.recv()
				#inputNode = self.socket.recv() #suveni
				#self.pubSub.nodes = eval(inputNode)#suveni
				#for name in self.pubSub.nodes:
				#	print ', '.join(str(item) for item in name)
				#logger.info(ack)
				logger.info('received the nodes from the eventserver ring')#suveni
				time.sleep(5)
			except:
				print("HBClient is gonna kill itself")
				sys.exit(0)

		logger.info('heartbeating stopped')
