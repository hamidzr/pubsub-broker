import time
import json

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
		msg = {'topic':self.topic,'body':self.body,'createdAt':self.createdAt}
		return msg
		# return "{0}, {1}, {2}".format(self.topic, self.body, self.createdAt)

	def __str__(self):
		# just for logging and reporting dont use to send messages
		return {'topic':self.topic,'body':self.body,'createdAt':self.createdAt}.__str__()

	@staticmethod
	def deSerialize(msg):
		# msg = json.loads(string)
		# eventArr = string.split(', ');
		return Event(msg['topic'],msg['body'],msg['createdAt'])
