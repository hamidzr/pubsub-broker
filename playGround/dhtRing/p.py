import zmq

address = '127.0.0.1'
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://" + address+ ":4444")

while True:
	topic = raw_input("enter a topic ")
	socket.send(topic)
	print socket.recv()