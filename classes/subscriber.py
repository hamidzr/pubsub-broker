import zmq
from random import randint
import logging
from classes.utils import *


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
	def __init__(self):
		# self.data = []
		# logging.basicConfig(filename="log/{}.log".format('S' + self.addr),level=logging.DEBUG)
		# connect to zk client
		self.isConnected = False
		self.zk = KazooClient(hosts='localhost:2181')
		self.zk.start()
		self.zk.add_listener(zk_listener)

	
	def register(self,newEsAddr ,topic):
		if self.isConnected:
			self.socket.disconnect("tcp://" + getPubFromAddress(self.esAddr))
			self.regSocket.disconnect("tcp://" + getPullFromAddress(self.esAddr))
		self.esAddr = newEsAddr		
		self.isConnected = True

		self.socket.connect("tcp://" + getPubFromAddress(self.esAddr))
		self.regSocket.connect("tcp://" + getPullFromAddress(self.esAddr))
		self.topic = topic #redundant?
		# create and ephimeral node
		self.zk.create("/ds/subs/sub-", self.__str__().encode('UTF8') ,ephemeral=True, sequence=True)
		self.regSocket.send_string("rs{}-{}, {}".format(self.sId, self.addr,topic))
		logger.info( 'register req sent')

	def subscribe(self, sFilter):
		# any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
		# system what it is interested in
		self.socket.setsockopt_string(zmq.SUBSCRIBE, sFilter.decode('ascii'))
		logger.info('subscription request to topic {} sent'.format(sFilter).decode('ascii'))
	def __str__(self):
		sub = {'topic':self.topic}
		return json.dumps(sub)