import threading
import logging
import sys
from classes.ringOrganizer import *
import zmq
from uhashring import HashRing
import json


# chord task is to keep/generate list like this. in an intelligent way to keep the ring up.


myIp = '127.0.0.1'
myPort = raw_input("what is my port ")
myAddress = myIp + ':' + myPort
myRoPort = str(int(myPort)-1000)

# helper function to get Ringorganizer address from es address
def getRoAddress(address):
	arr = address.split(':')
	port = int(arr[1])-1000
	return "{}:{}".format(arr[0],port)

context = zmq.Context()
repSocket = context.socket(zmq.REP)
repSocket.bind("tcp://*:" + myPort)
reqSocket = context.socket(zmq.REQ)

mHashRing = HashRing(nodes=[myAddress])
mRingOrganizer = ringOrganizer(mHashRing, myRoPort);
mRingOrganizer.nodes.add(myAddress)

# if arguments are passed => this is a joining node
if len(sys.argv) > 1:
	# get neighbor address
	nPort = raw_input("neighbor port")
	neighborAddress = '127.0.0.1:'+nPort
	# add it to our own nodesTable
	mRingOrganizer.nodes.add(neighborAddress)
	mHashRing.add_node(neighborAddress)
	# notify the neighbor to add us to it's table
	msg = {'type': 'nodeJoinReq', 'address':myAddress}
	#connect to neighborRingOrganizer
	reqSocket.connect("tcp://"+getRoAddress(neighborAddress))
	reqSocket.send(json.dumps(msg))
	suggestedNodes = reqSocket.recv()
	reqSocket.disconnect("tcp://"+getRoAddress(neighborAddress))
	# TODO make this recursive
	for nodeAddress in suggestedNodes.split(', '):
		# if I dont know this node
		if (nodeAddress not in mRingOrganizer.nodes):
			mRingOrganizer.nodes.add(nodeAddress)
			mHashRing.add_node(nodeAddress)
			reqSocket.connect("tcp://"+getRoAddress(nodeAddress))
			reqSocket.send(json.dumps(msg))
			print('more suggestions: ', reqSocket.recv())
			reqSocket.disconnect("tcp://"+getRoAddress(nodeAddress))


mRingOrganizer.start()


while True:
	key = repSocket.recv()
	selectedEs = mHashRing.get_node(key) # get the appropriate node
	msg = {'type': 'lookupReply', 'esAddress': selectedEs}
	repSocket.send(json.dumps(msg))
