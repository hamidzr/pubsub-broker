from classes.publisher import *

p1 = Publisher()
e1 = Event('topic a','body a')
p1.publish(e1)