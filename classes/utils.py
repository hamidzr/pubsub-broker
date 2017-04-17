# a set of utilites 

#  generate different address:ports off of a single adddress

import logging
from kazoo.client import KazooClient
import json

logger = logging.getLogger(__name__)


def getPortFromAddress(address):
	return int(address.split(':')[1])
def changePortBy(address,change):
	ip = address.split(':')[0]
	port = getPortFromAddress(address)
	port = str(port + change)
	return ip + ':' + port

def getHbClientFromAddress(address):
	addr = changePortBy(address,-1000)
	logger.info('hbClient addr: ' + addr)
	return addr
def getRingOrgFromAddress(address):
	addr = changePortBy(address,-2000)
	logger.info('RingOrg addr: ' + addr)
	return addr
def getHbServerFromAddress(address):
	addr = changePortBy(address,1000)
	logger.info('HbServer addr: ' + addr)
	return addr
def getPubFromAddress(address):
	addr = changePortBy(address,2000)
	logger.info('Publishing addr: ' + addr)
	return addr
def getPullFromAddress(address):
	addr = changePortBy(address,1500)
	logger.info('pullSocket addr: ' + addr)
	return addr



# ZK
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

# get the current leader and maybe watch for changes on the leader? 
# pre: a zookeeper instance with the node '/ds/ess'
# post: returns the node address for the child with lowest sequence number as leader
def getLeadingEs(zk):
	ess = zk.get_children('/ds/ess')
	ess.sort()
	return '/ds/ess/'+ess[0]

def getNodeData(zk,node_path):
	data,stat = zk.get(node_path)
	return json.loads(data)

# watches current leader and if there is a new leader does sth.
def watchLeader(zk,node_path):
	@zk.DataWatch(node_path)
	def my_func(data,stat):
		leader = getLeadingEs(zk)
		print("new leader is",getNodeData(zk,leader))
		# todo somehow let pub and sub handle 