import zmq
import threading
import time

class heartbeatClient (threading.Thread):

	def __init__(self, pId, servAddr):
		threading.Thread.__init__(self)
		self.pId = pId
		self.servAddr = servAddr
		context = zmq.Context()
		socket = context.socket(zmq.REQ)
		self.socket.connect("udp://" + servAddr+ ":4444")

	def run(self):
		print 'we are alive'
		while True:
			socket.send(b"hi")
			ack = socket.recv()
			time.sleep(5)	
		print 'heartbeating stopped'
