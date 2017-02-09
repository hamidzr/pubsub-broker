import zmq
import threading
import time

class heartbeatServer (threading.Thread):

	daemon = True # make it a deamon
	clients = {}

	def __init__(self, eventServer):
		threading.Thread.__init__(self)
		context = zmq.Context()
		self.eventServer = eventServer # get a handle on eventServer
		self.socket = context.socket(zmq.REP)
		self.socket.bind("tcp://*:4444")

	def run(self):
		print 'listening for heartbeats'
		while True:
			client_id = self.socket.recv()
			self.clients[client_id] = time.time()
			print ' heartbeat received from publisher'
			self.socket.send(b"ok")
			deadClientsArr = self.checkDeadClients()	
			print  deadClientsArr		
			for dClient in deadClientsArr:
				# TODO remove from dominant publishers and history
				# CALL undergister method
				self.eventServer.dominantPublishersSet.discard(dClient)

		print 'heartbeat server done'

	def checkDeadClients(self):
		print 'current clients are'
		print self.clients
		current_time = time.time() #aprox
		deadClients = []
		# find dead clients
		for key, val in self.clients.iteritems():
			if current_time - val > 10:
				deadClients.append(key)
		
		for dc in deadClients:
			print "{} is dead".format(dc)
			self.clients.pop(dc)
		return deadClients