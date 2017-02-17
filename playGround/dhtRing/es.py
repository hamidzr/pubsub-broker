import threading
import logging
import sys
from classes.dataStorage import *
import zmq
from uhashring import HashRing


# chord task is to keep/generate list like this. in an intelligent way to keep the ring up.

hr = HashRing(nodes=['myAddress'])
hr.add_node('10.2')



while True:
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://*:4444")
	key = socket.recv()

	selectedEs = hr.get_node(key)
	socket.send('register to ' + selectedEs)
