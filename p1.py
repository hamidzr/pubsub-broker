from classes.publisher import *
import time

#create a publisher and pass in intial configuration
p1 = Publisher('127.0.0.1:5555',1)

# keep publishing
while True:
	e1 = Event('topic a','body a')
	p1.publish(e1)
	# sleep for 300ms
	time.sleep(0.3)