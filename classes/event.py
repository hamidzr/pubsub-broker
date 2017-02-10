import time

class Event:
	# attribiutes
	# QUESTION do  I define these here or in the constructor?
	# id
	topic = 'unknown'
	# createdAt
	# might have better solution
	body = 'body'
	
	# constructor
	def __init__(self,topic,body , createdAt = time.time()):
		self.topic = topic
		self.body = body
		self.createdAt = time.time()

	# use json for this task?
	def serialize(self):
		return "{0}, {1}, {2}".format(self.topic, self.body, self.createdAt)

	@staticmethod
	def deSerialize(string):
		eventArr = string.split(', ');
		return Event(eventArr[0],eventArr[1],eventArr[2])
