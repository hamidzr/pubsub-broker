import zmq
from random import randint
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) #Q will this make it shared between all objects?
hdlr = logging.FileHandler('subscriber.log',mode='w')
logger.addHandler(hdlr)

class Subscriber:
	# attribiutes
	sId = randint(0,999)
	addr = str(randint(1000,9999))
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
		# TODO address = lookup(topic)
		self.regSocket.send_string("rs{}-{}, {}".format(self.sId, self.addr,topic))
		logger.info( 'register req sent')

	def lookup(self,key):
		# TODO call to any known eventservice (ring node) to findout where it should register. 
		# return: ES address (ip:port)
		pass

	def subscribe(self, sFilter):
		# any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
		# system what it is interested in
		self.socket.setsockopt_string(zmq.SUBSCRIBE, sFilter.decode('ascii'))
		logger.info('subscription request to topic {} sent'.format(sFilter).decode('ascii'))