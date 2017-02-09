import zmq
import threading
import time

class heartbeatClient (threading.Thread):

	daemon = True # make it a deamon

	def __init__(self, pId, servAddr):
		threading.Thread.__init__(self)
		self.pId = pId
		self.servAddr = servAddr
		context = zmq.Context()
		self.socket = context.socket(zmq.REQ)
		self.socket.connect("tcp://" + servAddr+ ":4444")

	def run(self):
		print 'we are alive'
		while True:
			self.socket.send(b"hi")
			ack = self.socket.recv()
			time.sleep(5)	
		print 'heartbeating stopped'
