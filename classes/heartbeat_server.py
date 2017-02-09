import zmq
import threading
import time

class heartbeatServer (threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		context = zmq.Context()
		socket = context.socket(zmq.REP)
		self.pullSocket.bind("tcp://*:4444")

	def run(self):
		print 'hearbeat server started'
		while True:
			hb = socket.recv()
			socket.send(b"ok")
		print 'heartbeat server done'
