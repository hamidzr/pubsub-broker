import time

class Event:
	# attribiutes
	# QUESTION do  I define these here or in the constructor?
	# id
	topic = 'unknown'
	# createdAt
	# might have better solution
	owner_strength = 1
	body = 'body'
	
	# constructor
	def __init__(self,topic,body , owner_strength=1,createdAt = time.time()):
		self.topic = topic
		self.body = body
		self.owner_strength = owner_strength
		self.createdAt = time.time()

	# use json for this task?
	def serialize(self):
		return "{0}, {1}, {2}, {3}".format(self.topic, self.body, self.owner_strength, self.createdAt)

	@staticmethod
	def deSerialize(string):
		eventArr = string.split(', ');
		return Event(eventArr[0],eventArr[1],eventArr[2],eventArr[3])