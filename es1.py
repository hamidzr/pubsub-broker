from classes.event_server import *
from classes.heartbeat_server import *

es1 = EventServer()
heartbeat_server = heartbeatServer()
heartbeatServer.start()
es1.start()