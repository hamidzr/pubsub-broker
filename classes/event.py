class Event:
	# attribiutes
	# createdAt
	# id
	topic = 'unknown'
	# might have better solution
	owner_strength = 1
	body = 'body'
	
	# constructor
	def __init__(self,topic,body, owner_strength=1):
		self.topic = topic
		self.body = body
		self.owner_strength = owner_strength

	def serialize(self):
		return "{0}, {1}, {2}".format(self.topic, self.body, self.owner_strength)

	@staticmethod
	def deSerialize(string):
		eventArr = string.split(', ');
		return Event(eventArr[0],eventArr[1],eventArr[2])