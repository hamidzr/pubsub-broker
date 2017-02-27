import zmq
import threading
import time
import logging
from classes.utils import *
import json


class heartbeatClient (threading.Thread):

	daemon = True # make it a deamon

	def __init__(self, pId, servAddr):
		threading.Thread.__init__(self)
		self.pId = pId
		self.servAddr = servAddr
		self.nodes={}
		context = zmq.Context()
		self.socket = context.socket(zmq.REQ)
		#Kevin added time out here
		self.socket.setsockopt(zmq.RCVTIMEO, 1000)
		#self.socket.setsockopt(zmq.SNDTIMEO, 1000)
		self.socket.connect("tcp://"+getHbServerFromAddress(servAddr))


	def resetAddress(self,servAddr):
		self.servAddr = servAddr
		self.socket.connect("tcp://" + getHbServerFromAddress(servAddr))

	def run(self):
		logging.basicConfig(level=logging.INFO)
		logger = logging.getLogger(__name__) #Q will this make it shared between all objects?
		hdlr = logging.FileHandler('heartbeatClient.log',mode='w')
		logger.addHandler(hdlr)
		
		logger.info( 'we are alive - heartbeating')
		while True:
			try:
				self.socket.send(b"{}".format(self.pId))
				ack = self.socket.recv()
				logger.info( ack)
				self.nodes=self.socket.recv()
			#modified by Kevin
			except :
				print ("Gonna notify other event_servers this one is dead")

				for nodeAddress in self.nodes.split(', '):
					if self.servAddr != nodeAddress :
						msg = {'type': 'nodeDeleteReq', 'address': self.servAddr}
					# connect to neighborRingOrganizer
						reqSocket = self.context.socket(zmq.REQ)
						reqSocket.connect("tcp://" + getRingOrgFromAddress(nodeAddress))
						reqSocket.send(json.dumps(msg))
				print ("time out! About to restart and re-register")

				

				#ask publisher to lookup() again and re-register, inside the re-register call , reset the servAddr of this
				#heartbeatClient

			logger.info( ack)
			time.sleep(5)	
		logger.info( 'heartbeating stopped')
