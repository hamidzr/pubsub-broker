import zmq

class Subscriber:
	# attribiutes
	interestedTopics = []

	context = zmq.Context()
	socket = context.socket(zmq.SUB)
	
	# constructor
	def __init__(self,esAddr = "127.0.0.1:5555"):
		# self.data = []
		self.socket.connect("tcp://" + esAddr)
		
	def subscribe(self, sFilter):
		# any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
		# system what it is interested in
		self.socket.setsockopt_string(zmq.SUBSCRIBE, sFilter.decode('ascii'))