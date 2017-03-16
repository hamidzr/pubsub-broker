import logging
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
def getSubFromAddress(address):
	addr = changePortBy(address,3000)
	logger.info('Sublishing addr: ' + addr)
	return addr