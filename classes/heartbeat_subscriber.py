import zmq
import threading
import time
import logging
import sys
from classes.utils import *
import json
from classes.event import *

class heartbeatSubscriber (threading.Thread):

    daemon = True
    # make it a deamon

    # def __init__(self, pId, servAddr)

    def __init__(self, sId, servAddr, subscriber):  # suveni
        threading.Thread.__init__(self)
        self.sId = sId
        self.servAddr = servAddr
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://" + getHbServerFromAddress(servAddr))
        self.socket.setsockopt(zmq.RCVTIMEO, 300)
        self.subscriber = subscriber  # suveni
        self.pubSocket = self.context.socket(zmq.PUB)
        self.pubSocket.connect("tcp://" + getSubFromAddress(subscriber.addr))
        #self.pubSocket.bind("tcp://" + getPubFromAddress(self.subscriber.addr))
        print('HBSUB binded addr: '+ getPubFromAddress(self.subscriber.addr))
    #def changeServAddr(self,servAddr):
	#	self.socket.disconnect("tcp://" + getHbServerFromAddress(self.servAddr))
	#	self.socket.close()
	#	self.socket = self.context.socket(zmq.REQ)
	#	#HeartbeatClient keeps sending message to HeartbeatServer without caring about the timeout
	#	#self.socket.setsockopt(zmq.RCVTIMEO, 1000)
	#	self.servAddr=servAddr
	#	self.socket.connectself.socket.connect("tcp://" + getHbServerFromAddress(self.servAddr))

    def run(self):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)  # Q will this make it shared between all objects?
        hdlr = logging.FileHandler('heartbeatClient.log', mode='w')
        logger.addHandler(hdlr)
        logger.info('we are alive - heartbeating')

        while True:
            try:
                self.socket.send(b"{}".format(self.sId))

                ack = self.socket.recv()
                # inputNode = self.socket.recv() #suveni
                # self.pubSub.nodes = eval(inputNode)#suveni
                # for name in self.pubSub.nodes:
                #	print ', '.join(str(item) for item in name)
                logger.info(ack)
                #logger.info('received the nodes from the eventserver ring')  # suveni
                time.sleep(5)
            except:
                print("HBClient is gonna kill itself")
                #e1=Event(self.publisher.topic, "ES is dead")
                msg = "{} {} {}".format(self.subscriber.topic, "-1",time.time())
                #msg = {'topic': self.subscriber.topic, 'body': 'ES is dead', 'createdAt': time.time()}
                self.subscriber.nodes.remove(self.servAddr)
                self.pubSocket.send_string(msg)
                self.pubSocket.disconnect(("tcp://" + getSubFromAddress(self.subscriber.addr)))
                self.pubSocket.close()
                print('I sent: '+msg)
                logger.info('heartbeating stopped')
                sys.exit(0)


