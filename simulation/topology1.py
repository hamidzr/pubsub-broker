from mininet.net import Mininet
from mininet.topo import Topo
from mininet.net import CLI
import random
from random import randint
import os
# IMPORTANT:  if the import is broken > README.md

# init
if not os.path.exists('log'):
    os.makedirs('log')
# TODO cleanup

# set options
proj_path = os.path.abspath('../')
es_address = '10.0.0.1:5555'
num_hosts = 10


topics = set(['books','news','compilers','tech','world','sport'])
publishers = set([])
subscribers = set([])

topo = Topo()  # Create an empty topology
topo.addSwitch("s1")  # Add switches and hosts to the topology
topo.addHost("es")
topo.addLink('es','s1')
print "adding n subscribers and publishers to the topology"
for h in range(num_hosts/2):
	publisher = topo.addHost("hp{}".format(h+1))
	topo.addLink(publisher, "s1") # Wire the switches and hosts together with links
	publishers.add(publisher)
	subscriber = topo.addHost("hs{}".format(h+1))
	topo.addLink(subscriber, "s1")
	subscribers.add(subscriber)

# print random.sample(topics,1)
print publishers
print subscribers


net = Mininet(topo)  # Create the Mininet, start it and try some stuff
net.start()
# net.pingAll()
es = net.get('es')
es.cmd("python {}/es1.py > log/es.log &".format(proj_path))

print 'instructing publishers'
for host in publishers:
	publisher = net.get(host)
	owner_strength = randint(1,3)
	topic = random.sample(topics,1)
	print 'starting publisher with topic {}, os {}'.format(topic,owner_strength)
	publisher.cmd("python {}/p1.py {} {} {} > log/{}.log &".format(proj_path,es_address,owner_strength,topic,host))

print 'instructing subscribers'
for host in subscribers:
	subscriber = net.get(host)
	topic = random.sample(topics,1)
	print 'starting subscriber with topic {}'.format(topic)
	subscriber.cmd("python {}/s1.py > log/{}.log &".format(proj_path,host))

CLI (net)
