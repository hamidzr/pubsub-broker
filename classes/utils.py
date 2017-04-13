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