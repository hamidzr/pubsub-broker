# cleanup zookeeper and make sure structure is in place
from kazoo.client import KazooClient
import sys
# import logging
# logging.basicConfig()

zk = KazooClient(hosts='localhost:2181')
zk.start()
# checks about zookeeper server
def zk_listener(state):
	if state == KazooState.LOST:
		# Register somewhere that the session was lost
		print('Zookeeper lost')
		pass
	elif state == KazooState.SUSPENDED:
		# Handle being disconnected from Zookeeper
		print('Zookeeper suspended')
		pass
	else:
		# Handle being connected/reconnected to Zookeeper
		pass


def printTopView(zk,root):
	if(zk.exists(root)):
		rootNodes = zk.get_children(root)
		print(rootNodes)
		for i in rootNodes:
			subRoots = zk.get_children(root+'/'+i)
			print('=========')
			for j in subRoots:
				print(j,'details',zk.get(root +'/'+ i + '/' + j))

zk.add_listener(zk_listener)
root_node = "/ds" # root node for this project
# print(zk.get_children(root_node))


if zk.exists(root_node):
	printTopView(zk,root_node)

	answ = raw_input('are you sure? (y/n)')
	if answ != 'y':
		sys.exit()
	print('cleaning all nodes')
	zk.delete(root_node,-1,True)
	print('deleted')
	zk.create("/ds",b"myData")
	zk.create("/ds/ess",b"myData")
	zk.create("/ds/pubs",b"myData")
	zk.create("/ds/subs",b"myData")
else:
	print('there was no node')
	zk.create("/ds",b"myData")
	zk.create("/ds/ess",b"myData")
	zk.create("/ds/pubs",b"myData")
	zk.create("/ds/subs",b"myData")

print(zk.get_children(root_node))
print(zk.get_children("/ds/ess"))
print(zk.get_children("/ds/pubs"))
print(zk.get_children("/ds/subs"))

print('Done, exiting')
zk.stop()
zk.close()
