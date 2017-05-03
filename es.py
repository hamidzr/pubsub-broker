from classes.event_server import *
import sys
# import signal # to handle ctrl-c termination to cleanup zookeeper


if sys.argv[1] == None:
	print('you need to pass in an address')
	sys.exit()
myAddress = sys.argv[1]

# watch for changes to publishers
es1 = EventServer(myAddress)
@es1.zk.ChildrenWatch('/ds/pubs')
def my_func(children):
    # get a list of current publisher's pId
    print('children are', children);
    newPIds = set([])
    for child in children:
    	data = getNodeData(es1.zk,'/ds/pubs/'+child)
    	newPIds.add(str(data['pId']))
    oldPIds = set([])
    for publisher in es1.publishers:
    	oldPIds.add(publisher.pId)
    print ('old',oldPIds,'new',newPIds)
    # calculate which publisher left ( if left )
    oldPIds.difference_update(newPIds)
    # print('leavers',oldPIds)

    # unregister leaving publisher
    for leaver in oldPIds:
    	es1.unregisterPublisher(leaver)

es1.start()
