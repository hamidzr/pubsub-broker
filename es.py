from classes.event_server import *
import sys
# import signal # to handle ctrl-c termination to cleanup zookeeper


if sys.argv[1] == None:
	print('you need to pass in an address')
	sys.exit()
myAddress = sys.argv[1]

es1 = EventServer(myAddress)
es1.start()
