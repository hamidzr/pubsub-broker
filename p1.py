from classes.publisher import *
from random import randint
import sys # to get cli args
import datetime
import logging
#create a publisher and pass in intial configuration

if len(sys.argv) == 4:
	# set the variables from the arguments passed	
	eventserver_address = sys.argv[1]
	topic = sys.argv[2]
	owner_strength = sys.argv[3]
else:
	logging.debug( 'no arguments provided, resorting to defaults')
	eventserver_address = '127.0.0.1:5555'
	owner_strength = 1
	topic = 'book'

p1 = Publisher(eventserver_address,owner_strength,topic)


#If not registered successfully, do it again
i=0
i=i+1
print("Count of registration:",i)
registered=p1.lookup(topic)

while not registered :
	i = i + 1
	print("Count of registration:", i)
	print("Registration failed, about to try again")

	registered = p1.lookup(topic)
	time.sleep(2)

# keep publishing
while True:
	body = "{}".format(randint(0,9))
	e1 = Event(p1.topic,body)
	if not p1.publish(e1):
		i = i + 1
		print("Yes, I call the registration here")
		print("Count of registration:", i)
		registered = p1.lookup(topic)

		while not registered:
			i = i + 1
			print("Count of registration:", i)
			registered = p1.lookup(topic)
			time.sleep(2)

	# sleep for 2s
	time.sleep(2)
