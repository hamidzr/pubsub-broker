import zmq

address = '127.0.0.1'
nodePort = raw_input('es port')
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://" + address+ ':' + nodePort)

while True:
	topic = raw_input("enter a topic ")
	socket.send(topic)
	print socket.recv()