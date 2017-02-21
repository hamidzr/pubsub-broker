import zmq
import threading
from uhashring import HashRing
import json
import time

class ringOrganizer(threading.Thread):
	"""docstring for ringOrganizer"""
	daemon = True # make it a deamon
	def __init__(self, hashRing, myPort):
		super(ringOrganizer, self).__init__()
		self.hr = hashRing
		context = zmq.Context()
		self.repSocket = context.socket(zmq.REP)
		self.repSocket.bind("tcp://*:" + myPort)
		self.nodes = set([])

	# def reqJoin(self,esAddress,destination):
	# 	# TODO change esAddress to es object
	# 	msg = {'type': 'nodeJoinReq', 'address':esAddress}

	def addNode(self,msg):
		self.hr.add_node(msg['address'])
		self.nodes.add(msg['address'])
		print 'node added: ', msg['address']
	
	def suggestNodes(self):
		return ', '.join(self.nodes)

	def run(self):
		print 'ringOrganizer started'
		while True:
			string = self.repSocket.recv()
			msg = json.loads(string)
			if msg['type']== 'nodeJoinReq':
				self.addNode(msg)
				suggestions = self.suggestNodes()
				self.repSocket.send_string(suggestions)


		