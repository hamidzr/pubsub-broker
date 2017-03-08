import random
import hashlib
import logging
import os

# init
keyLength = 8 # the number of bits in the key # QUESTION there should be consequenses if this is far bigger than the number of our nodes




class Node(object):
	"""docstring for Node"""
	def __init__(self, name):
		super(Node, self).__init__()
		self.id = os.urandom(1 << 20) #random.getrandbits(keyLength) # generate a random k bit hash as ID for nodes
		self.pos = position(self.id)
		self.next = None
		self.prev = None
		self.data = {}
		self.name = str(name)
	def __str__(self):
		return self.name + ' position: '+ str(self.pos) +' data: ' + self.data.__str__()






# calculate the distance key from node
def distance(nodeId, key):
	nodeHash = position(nodeId)
	keyHash = position(key)
	print("key position: ", keyHash)
	distance = None;
	if nodeHash==keyHash:
		distance = 0
	elif nodeHash>keyHash:
		distance = nodeHash-keyHash
	elif keyHash > nodeHash: # this means that a is located after b ( a is bigger )
		distance = (2**keyLength)-(keyHash-nodeHash)
	else: #redundant
		distance = False
	print("calculated distance: ", distance)
	return distance

# make a kbit hash out of a key
def position(key):
	# sha1 return 160bit keys. md5 128
	key = str(key)
	res = int(hashlib.md5(key).hexdigest(),16) % 2**keyLength #convert to int with base 16
	return res


#helper func: move the keys and the data from one node to the other
#keys: array of keys
def moveKeys(keys,source,destination):
	print("moving keys",keys)
	for key in keys:
		destination.data[key] = source.data[key]
		del source.data[key]

# From the start node, find the node responsible
# for the target key
def findSuccessor(startNode, key):
	# # suggested but buggy findSuccessor
	# current=startNode
	# while distance(current.id, key) > distance(current.next.id, key):
	# 	current=current.next
	# 	print ('searching for successor NEVER RUNS')
	# return current
	# #
	curNode = startNode.next
	lowestDistance = distance(startNode.id, key)
	theNode = startNode
	while startNode.id != curNode.id:
		if distance(curNode.id, key) < lowestDistance:
			lowestDistance = distance(curNode.id, key)
			theNode = curNode
		curNode = curNode.next
	print('the successor is {} - distance: {}'.format(theNode,lowestDistance))
	return theNode
	
# Find the responsible node and get the value for
# the key
def get(startNode, key):
	node=findSuccessor(startNode, key)
	if key in node.data:
		print("getting the data for key {} from node {}".format(key,node))
		return node.data[key]
	else:
		print("key {} - {} is not set on {}".format(key,position(key),node))
		return False

# Find the responsible node and set the value
# with the key
def set(startNode, key, value):
	node=findSuccessor(startNode, key)
	node.data[key]=value
	print("set the key {} - {} to value {} on node {}".format(key,position(key),value,node))


#let nodes join to an existing ring of nodes. can be turned into a method on node
def join(startNode,newNode):
	print("node",newNode.__str__(),"is joining.")
	print(ringToString(startNode))
	#put the new node in its position
	suc = findSuccessor(startNode,newNode.id)
	prev = suc.prev

	#move the appropriate keys to itself from successor
	toMove = []
	for key in suc.data:
		# TODO hash the nodeId only once
		# if position(key) > position(newNode.id):
		if position(key) <= position(newNode.id):
			toMove.append(key)
			print('moving',key,'from',suc.name,'to',newNode.name)
		else:
			print(key, ' stays in the node, no need to move it')
	moveKeys(toMove,suc,newNode)
	# moveKeys(suc.data.keys(),suc,newNode)

	#update the nodes pointers to point to this newNode (the tables)
	newNode.prev = prev
	newNode.next = suc
	prev.next = newNode
	suc.prev = newNode
	print(ringToString(startNode))

#facilitates leaving of a node from the ring.
def leave(leavingNode):
	print("node",leavingNode.__str__(),"is leaving.")
	suc = leavingNode.next
	pred = leavingNode.prev
	print(ringToString(suc))
	moveKeys(leavingNode.data.keys(),leavingNode,suc)
	pred.next = suc
	suc.prev = pred
	print(ringToString(suc))

#show a visual of the ring for debugging purposes
def ringToString(node):
	string = ''
	for x in xrange(1,10):
		string += node.__str__() + "\n"
		node = node.next
	return string

# some test objects to work with
n1 = Node('0')
n1.next = n1
n1.prev = n1


c = 1
for x in xrange(1,7):
	join(n1,Node(c))
	c = c+1

set(n1,'hamid','theOne')
print(ringToString(n1))
while True:
	inp = raw_input("input: ")
	if inp == 'addNode':
		join(n1,Node(c))
		c += 1
	elif inp == 'show':
		print(ringToString(n1))
	elif inp == 'delNode':
		node = findSuccessor(n1,raw_input("key to del the node "))
		leave(node)
	else:
		val = get(n1, inp)
		if val:
			print val
		else:
			val = raw_input("value: ")
			set(n1,inp,val)
