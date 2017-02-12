import zmq
import threading
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) #Q will this make it shared between all objects?
hdlr = logging.FileHandler('heartbeatServer.log',mode='w')
logger.addHandler(hdlr)

class heartbeatServer (threading.Thread):

	daemon = True # make it a deamon
	clients = {}

	def __init__(self, eventServer):
		threading.Thread.__init__(self)
		context = zmq.Context()
		self.eventServer = eventServer # get a handle on eventServer
		self.socket = context.socket(zmq.REP)
		self.socket.bind("tcp://*:4444")
		# logging.basicConfig(filename="log/{}hbServer.log".format(self.addr),level=logging.DEBUG)

	def run(self):
		logging.debug( 'listening for heartbeats')
		while True:
			client_id = self.socket.recv()
			self.clients[client_id] = time.time()
			logger.info( ' heartbeat received from publisher')
			self.socket.send(b"ok")
			deadClientsArr = self.checkDeadClients()	
			logger.info(  deadClientsArr		)
			for dClient in deadClientsArr:
				# TODO remove from dominant publishers and history
				# CALL undergister method
				self.eventServer.unregisterPublisher(dClient)

		logger.info( 'heartbeat server done')

	def checkDeadClients(self):
		logger.info( 'current clients are')
		logger.info( self.clients)
		current_time = time.time() #aprox
		deadClients = []
		# find dead clients
		for key, val in self.clients.iteritems():
			if current_time - val > 10:
				deadClients.append(key)
		
		for dc in deadClients:
			logger.warning( "{} is dead".format(dc))
			self.clients.pop(dc)
		return deadClients