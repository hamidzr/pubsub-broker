import threading
import time
import logging

# exitFlag = 0

# class heartbeat (threading.Thread):
# 	def __init__(self, pId, esAddr):
# 		threading.Thread.__init__(self)
# 		self.pId = pId
# 		self.esAddr = esAddr

# 	def run(self):
# 		print 'thread running'
# 		time.sleep(1)
# 		print 'thread done'




# t1 = heartbeat(1,2)
# t1.start()
# print 'tada'
# t1.join()
print 'done'
logging.warning('warning')
logging.info('info')
logging.debug('debug')
a = {'a':'asdf'}
logging.warning(a)