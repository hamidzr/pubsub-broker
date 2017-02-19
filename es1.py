from uhashring import HashRing
from classes.event_server import *
from classes.ringOrganizer import *
import sys

myAddress = sys.argv[1]
es1 = EventServer(myAddress)

if len(sys.argv) > 2:
	# get neighbor address
	neighborAddress = sys.argv[2]
	es1.joinNotifyNode(neighborAddress)


es1.start()