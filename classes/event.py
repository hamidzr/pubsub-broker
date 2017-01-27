class Event:
	# attribiutes
	# createdAt
	# id
	topic = 'unknown'
	body = 'body'
	
	# constructor
	def __init__(self,topic,body):
		self.topic = topic
		self.body = body

	def toString(self):
		return "{0}, {1}".format(self.topic, self.body)