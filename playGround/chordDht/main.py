import random
import hashlib
import logging
import os

# init
KEYLENGTH = 6 # the number of bits in the key # QUESTION there should be consequenses if this is far bigger than the number of our nodes



# TODO refactor related fundtionalities to its own class
class Node(object):
	"""docstring for Node"""
	def __init__(self, name):
		super(Node, self).__init__()
		self.id = os.urandom(1 << 20) #random.getrandbits(KEYLENGTH) # generate a random k bit hash as ID for nodes
		self.pos = position(self.id)
		self.fTable = [self]*KEYLENGTH  # consider changing to another structure to store more successors
		self.pred = None # predecessor
		self.data = {}
		self.name = str(name)
		# have and maintain a self.successor?

	def __str__(self):
		return 'node: '+ self.name + ' position: '+ str(self.pos) +' data: ' + self.data.__str__() + ' fTable: ' + self.vFTable()
	
	def genFingerTable(self):
		# self.fTable = [] # null it out for now
		maxKey = 2**KEYLENGTH
		for i in xrange(0,KEYLENGTH):
			suc = findSuccessor(self,(self.pos + 2**i) % maxKey)
			self.fTable[i] = suc

	# returns a view of the fingertable
	def vFTable(self):
		view = ""
		for x in self.fTable:
			if isinstance(x,Node):
				view += str(x.pos) + ", "
			else:
				view += "None "
		return view

	def chFindSuccessor(self,pos):
		print('asking node with pos {} to find suc for {}'.format(self.pos,pos))
		if self.pos == self.fTable[0].pos:
			print('WARNING badim khodame  ') #should never see this
		# check if the next node is the suc
		if pos > self.pos and pos <= self.fTable[0].pos:
			return self.fTable[0]
		# elif pos <= self.fTable[0].pos and pos < self.pos and isTheBiggest(self):
		# 	return self
		else:
			node = self.closestPrecedingNode(pos)
			return node.chFindSuccessor(pos)

	# search the local table for highest predecessor of Id
	def closestPrecedingNode(self,pos):
		# QUESTION: the alg from the paper can't find the closest preceding node.
		# print(self.vFTable())
		# for i in xrange(KEYLENGTH-1,-1,-1):
		# 	# if self.fTable[i].pos < self.pos and  self.fTable[i].pos < pos:
		# 	# 	raw_input('peyda kard {}'.format(self.fTable[i]))
		# 	# 	return self.fTable[i]
		# 	if self.fTable[i].pos > self.pos and self.fTable[i].pos < pos:
		# 		raw_input('peyda kard {}'.format(self.fTable[i]))
		# 		return self.fTable[i]
		# raw_input('couldnt find closest')
		# return self

		closestPNode = findClosest(pos,self.fTable)
		print('next jump is to: ',closestPNode.__str__())
		raw_input("press enter to continue jumping")
		return closestPNode

	#another way to find suc (not complete)
	def fsbak(self,key):
		# check if we are the suc
		if key in self.data.keys():
			return self
		else:
			pos = position(key)
			for i in xrange(1,KEYLENGTH):
				if self.fTable[0] and self.fTable[0]:
					pass

#tmp check if is the biggest in its ftable
def isTheBiggest(node):
	res = True
	for x in node.fTable:
		if x >= node.pos:
			res = False
	return res

#alternative closestPreceidingNode. 
# gets an array of positions ( generated from a fingertable )
# returns ---- preceding node of a fingerTable to a pos(of a key)
def findClosest(pos,fTable):
	fTable.sort(key=lambda x: x.pos, reverse=False)
	closestI = len(fTable)-1
	for indx,val in enumerate(fTable):
		if val.pos > pos:
			closestI = len(fTable)-1 if indx == 0 else indx -1
			break
	print('next jump is to pos {} which is node: {}'.format(fTable[closestI].pos,fTable[closestI]))
	return fTable[closestI]

# calculate the distance key from node
def distance(nodePos, keyPos):
	# print("key position: ", keyPos)
	distance = None;
	if nodePos==keyPos:
		distance = 0
	elif nodePos>keyPos:
		distance = nodePos-keyPos
	elif keyPos > nodePos: # this means that a is located after b ( a is bigger )
		distance = (2**KEYLENGTH)-(keyPos-nodePos)
	else: #redundant
		distance = False
	# print("calculated distance: ", distance)
	return distance

# make a kbit hash out of a key
def position(key):
	# sha1 return 160bit keys. md5 128
	key = str(key)
	res = int(hashlib.md5(key).hexdigest(),16) % 2**KEYLENGTH #convert to int with base 16
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
def findSuccessor(startNode, pos):
	curNode = startNode.fTable[0]
	lowestDistance = distance(startNode.pos, pos)
	theNode = startNode
	while startNode.id != curNode.id:
		if distance(curNode.pos, pos) < lowestDistance:
			lowestDistance = distance(curNode.pos, pos)
			theNode = curNode
		curNode = curNode.fTable[0]
	# print('the successor is {} - distance: {}'.format(theNode,lowestDistance))
	return theNode
	


# Find the responsible node and get the value for
# the key
def get(startNode, key):
	node=findSuccessor(startNode, position(key))
	if key in node.data:
		print("getting the data for key {} from node {}".format(key,node))
		return node.data[key]
	else:
		print("key {} - {} is not set on {}".format(key,position(key),node))
		return False

# Find the responsible node and set the value
# with the key
def set(startNode, key, value):
	node=findSuccessor(startNode, position(key))
	node.data[key]=value
	print("set the key {} - {} to value {} on node {}".format(key,position(key),value,node))


#let nodes join to an existing ring of nodes. can be turned into a method on node
def join(startNode,newNode):
	print(newNode.__str__(),"is joining.")
	print(ringToString(startNode))
	#put the new node in its position
	suc = findSuccessor(startNode,newNode.pos)
	pred = suc.pred

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
	newNode.pred = pred
	newNode.fTable[0] = suc
	pred.fTable[0] = newNode
	suc.pred = newNode
	print(ringToString(startNode))

#facilitates leaving of a node from the ring.
def leave(leavingNode):
	print("node",leavingNode.__str__(),"is leaving.")
	suc = leavingNode.fTable[0]
	pred = leavingNode.pred
	print(ringToString(suc))
	moveKeys(leavingNode.data.keys(),leavingNode,suc)
	pred.fTable[0] = suc
	suc.pred = pred
	print(ringToString(suc))


#show a visual representation of the ring for debugging purposes
def ringToString(node):
	print("generating a view of first 10 items nodes in the ring: ")
	string = ''
	# this might generate some repetition for now. if n less than 10
	for x in xrange(1,10):
		string += node.__str__() + "\n"
		node.genFingerTable() # CHANGE use this to keep the ftables updated for now
		node = node.fTable[0]
	return string


# some test objects to work with
n1 = Node('0')
n1.pred = n1

n1.fTable[0] = n1
c = 1
for x in xrange(1,8):
	join(n1,Node(c))
	c = c+1

# set(n1,'h','theOne')
print(ringToString(n1))

while True:
	inp = raw_input("input: ")
	if inp == 'addNode':
		join(n1,Node(c))
		c += 1
	elif inp == 'show':
		print(ringToString(n1))
	elif inp == 'delNode':
		node = findSuccessor(n1,position(raw_input("key to del the node ")))
		leave(node)
	elif inp == 'fs':
		node = findSuccessor(n1,int(raw_input("find suc for a position (asking node1 ): ")))
		print node
	elif inp == 'cs':
		node = n1.chFindSuccessor(int(raw_input("find suc for a position (asking node1 ): ")))
		print node
	elif inp == 'pos':
		print position(raw_input("get the position of this: "))
	else:
		val = get(n1, inp)
		if val:
			print val
		else:
			val = raw_input("value: ")
			set(n1,inp,val)
