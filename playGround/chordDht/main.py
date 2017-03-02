import random
import hashlib
import logging

# init
keyLength = 160 # the number of bits in the key




class Node(object):
	"""docstring for Node"""
	def __init__(self, name):
		super(Node, self).__init__()
		self.id = random.randint(10000,99999) #random.getrandbits(keyLength) # generate a random k bit hash as ID for nodes
		self.next = None
		self.prev = None
		self.data = {}
		self.name = str(name)
	def __str__(self):
		return self.name + ' data: ' + self.data.__str__()






# calculate the distance key from node
def distance(nodeId, key):
	nodeHash = hashKey(nodeId)
	keyHash = hashKey(key)
	print 'calculating node '
	if nodeHash==keyHash:
		return 0
	elif nodeHash>keyHash:
		return nodeHash-keyHash
	else: # this means that a is located after b ( a is bigger )
		return (2**keyLength)+(keyHash-nodeHash)

# make a kbit hash out of a key
def hashKey(key):
	# sha1 return 160bit keys. md5 128
	key = str(key)
	return long(hashlib.sha1(key).hexdigest(),16) #convert to long with base 16



# From the start node, find the node responsible
# for the target key
def findSuccessor(startNode, key):
	## suggested but buggy findSuccessor
	# current=startNode
	# while distance(current.id, key) > distance(current.next.id, key):
	# 	current=current.next
	# 	print ('searching for successor')
	# return current
	##
	curNode = startNode.next
	lowestDistance = distance(startNode.id, key)
	theNode = curNode
	while startNode.id != curNode.id:
		if distance(curNode.id, key) < lowestDistance:
			lowestDistance = distance(curNode.id, key)
			theNode = curNode
		curNode = curNode.next

	print('the successor for key {} is {}'.format(key,theNode))
	return theNode
	
# Find the responsible node and get the value for
# the key
def get(startNode, key):
	node=findSuccessor(startNode, key)
	if key in node.data:
		print("getting the data for key {} from node {}".format(key,node))
		return node.data[key]
	else:
		print("key {} is not set on {}".format(key,node))
		return False

# Find the responsible node and set the value
# with the key
def set(startNode, key, value):
	node=findSuccessor(startNode, key)
	node.data[key]=value
	print("set the key {} to value {} on node {}".format(key,value,node))


#let nodes join to an existing ring of nodes. can be turned into a method on node
def join(startNode,newNode):
	print(ringToString(startNode))
	#put the new node in its position
	suc = findSuccessor(startNode,newNode.id)
	prev = suc.prev

	#move the appropriate keys to itself from successor
	toMove = []
	for key in suc.data:
		# TODO hash the nodeId only once
		# if hashKey(key) > hashKey(newNode.id):
		if hashKey(key) <= hashKey(newNode.id): #TODO THIS LINE SHOULD BE THE WORKING ONE
			toMove.append(key)
		else:
			print(key, ' stays in the node, no need to move it')
	for key in toMove:
		#move the key and its data to the newNode
		print('moving',key,'from',suc.name,'to',newNode.name)
		newNode.data[key] = suc.data[key]
		del suc.data[key]

	#update the nodes pointers to point to this newNode (the tables)
	newNode.prev = prev
	newNode.next = suc
	prev.next = newNode
	suc.prev = newNode
	print(ringToString(startNode))

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
for x in xrange(1,4):
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
	else:
		val = get(n1, inp)
		if val:
			print val
		else:
			val = raw_input("value: ")
			set(n1,inp,val)
