from classes.publisher import *
import time

p1 = Publisher()
# keep publishing
while True:
	e1 = Event('topic a','body a')
	p1.publish(e1)
	# sleep for 300ms
	time.sleep(0.3)