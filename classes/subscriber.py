import zmq
from random import randint
import logging

class Subscriber:
	# attribiutes
	sId = randint(0,999)
	addr = str(randint(10000,9999))
	# addr = commands.getstatusoutput("ifconfig | awk '/inet addr/{print substr($2,6)}' | sed -n '1p'")[1]
	context = zmq.Context()
	socket = context.socket(zmq.SUB)
	regSocket = context.socket(zmq.PUSH)

	
	# constructor
	def __init__(self,esAddr = "127.0.0.1"):
		# self.data = []
		self.socket.connect("tcp://" + esAddr + ":6666")
		self.regSocket.connect("tcp://" + esAddr + ":5555")
		# logging.basicConfig(filename="log/{}.log".format('S' + self.addr),level=logging.DEBUG)
	
	def register(self,topic):
		pass
		# TODO : SEND AN ID LIKE PUBLISHER
		self.regSocket.send_string("rs{}-{}, {}".format(self.sId, self.addr,topic))
		print 'register req sent'

	def subscribe(self, sFilter):
		# any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
		# system what it is interested in
		self.socket.setsockopt_string(zmq.SUBSCRIBE, sFilter.decode('ascii'))