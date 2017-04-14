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
		print('top nodes', rootNodes)
		for i in rootNodes:
			subRoots = zk.get_children(root+'/'+i)
			print('=========' + i + '========')
			for j in subRoots:
				data,stat = zk.get(root +'/'+ i + '/' + j)
				print(j,'metadata: ', data)

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
else:
	print('there was no node')

zk.create("/ds",b"myData")
zk.create("/ds/ess",b"myData")
zk.create("/ds/pubs",b"myData")
zk.create("/ds/subs",b"myData")
# zk.create("/ds/eselection",b"myData")
printTopView(zk,root_node)


print('Done, exiting')
zk.stop()
zk.close()
