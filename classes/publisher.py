import zmq
from classes.event import *
# from classes.heartbeat_client import *
from random import randint
import logging
from classes.utils import *

# assumptions:
# 	only one topic per publisher
# 	
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__) #Q will this make it shared between all objects?
hdlr = logging.FileHandler('publisher.log',mode='w')
logger.addHandler(hdlr)

class Publisher:
	# attribiutes
	addr = str(randint(1000,9999))
	# addr = commands.getstatusoutput("ifconfig | awk '/inet addr/{print substr($2,6)}' | sed -n '1p'")[1]
	pId = randint(0,999)
	context = zmq.Context()
	socket = context.socket(zmq.PUSH)
	topic = 'unknown'
    # constructor
	def __init__(self, strength ,topic):
		# self.data = []
		self.topic = topic
		self.strength = strength
		self.isConnected = False
		# connect to zk client
		self.zk = KazooClient(hosts='localhost:2181')
		self.zk.start()
		self.zk.add_listener(zk_listener)
		# create and ephimeral node
		self.zk.create("/ds/pubs/pub-", self.__str__().encode('UTF8') ,ephemeral=True, sequence=True)

	def register(self,newEsAddr):
		# heartbeatClient(self.pId,self.esAddr).start()
		if self.isConnected:
			self.socket.disconnect("tcp://" + getPullFromAddress(self.esAddr))
		self.esAddr = newEsAddr		
		self.isConnected = True
		self.socket.connect("tcp://" + getPullFromAddress(newEsAddr)) #5555
		self.socket.send_string("rp{}-{}, {}, {}".format(self.pId, self.addr,self.topic,self.strength))
		logger.info('register request sent')

	
	def publish(self, event):
		self.socket.send_string("ev{}-{}".format(self.pId, event.serialize()))
		logger.info('published: ' + event.serialize())

	def __str__(self):
		publisher = {'topic':self.topic,'os':self.strength} 
		return json.dumps(publisher)
