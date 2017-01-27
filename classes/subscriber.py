import zmq

class Subscriber:
	# attribiutes
    interestedTopics = []

    # constructor
    def __init__(self,esAddr = "127.0.0.1:5556"):
    	# self.data = []
		#  Socket to talk to server
		context = zmq.Context()
		# Since we are the subscriber, we use the SUB type of the socket
		socket = context.socket(zmq.SUB)
		connect_str = "tcp://" + esAddr
		socket.connect(connect_str)
    	
	def subscribe(self, sFilter):
		# any subscriber must use the SUBSCRIBE to set a subscription, i.e., tell the
		# system what it is interested in
		socket.setsockopt_string(zmq.SUBSCRIBE, sFilter)
		while true:
			string = socket.recv_string()
			print(string)
