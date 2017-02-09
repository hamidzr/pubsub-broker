import zmq
import threading
import time

class heartbeatServer (threading.Thread):

	daemon = True # make it a deamon

	def __init__(self):
		threading.Thread.__init__(self)
		context = zmq.Context()
		self.socket = context.socket(zmq.REP)
		self.socket.bind("tcp://*:4444")

	def run(self):
		print 'listening for heartbeats'
		while True:
			hb = self.socket.recv()
			print hb + ' heartbeat received from publisher'
			self.socket.send(b"ok")
		print 'heartbeat server done'
