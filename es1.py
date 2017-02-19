from uhashring import HashRing
from classes.event_server import *
from classes.ringOrganizer import *

es1 = EventServer('127.0.0.1:5555')
es1.start()