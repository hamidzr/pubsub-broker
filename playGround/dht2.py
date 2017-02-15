import threading
import time
import logging
from hash_ring import *
import sys

#using hash_ring package

class DataStorage(object):
    """docstring for DataStorage"""
    def __init__(self,name):
        super(DataStorage, self).__init__()
        self.dic = {}
        self.name = name
    def __str__(self):
        return self.name # whatever we wanna hash
    """ set a key value
    returns true if succeed """
    def set(self,key,value):
        self.dic[key] = value
        return key, value + ' successfully added to DataStorage ' + self.name
    def displayData(self):
        return self.name + ' ' + self.dic.__str__()
    def get(key):
        return self.dic[key]


ds1 = DataStorage('ds1')
ds1.set('ali','30')
        
ds2 = DataStorage('ds2')
ds2.set('lisa','25')

ds3 = DataStorage('ds3')
ds3.set('jack','25')

ds4 = DataStorage('ds4')
ds4.set('jhon','25')


ring = HashRing([ds1, ds2, ds3, ds4]) # pass stringalbe items

# topic = 'a'
# print 'topic',topic,'node position', ring.get_node_pos(topic)
# print 'topic',topic,'node ', ring.get_node(topic)
# iterator =  ring.iterate_nodes(topic, True)
# for node in iterator:
# 	print node

name = "hamid"
age = '24'

# name = sys.argv[1] || "hamid"
name = sys.argv[1]
age = sys.argv[2]

selectedDs = ring.get_node(name)
selectedDs.set(name,age)

print selectedDs.displayData()

# mc = MemcacheRing(['127.0.0.1:11212'])
# mc.set('hello', 'world')
# print mc.get('hello')