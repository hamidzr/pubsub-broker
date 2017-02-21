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
es_address = '10.0.0.1'
num_hosts = int(raw_input("input the total number of hosts: "))


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

commandsFile = open('commands.log','w')

net = Mininet(topo)  # Create the Mininet, start it and try some stuff
net.start()
# net.pingAll()
# 
commandsFile.write('es ' + "python {}/es1.py &".format(proj_path))

print 'instructing publishers'
for host in publishers:
	# publisher = net.get(host)
	owner_strength = randint(1,3)
	topic = random.sample(topics,1)
	print 'adding publisher command with topic {}, os {}'.format(topic,owner_strength)
	command = "python {}/p1.py {} {} {} &".format(proj_path,es_address,topic,owner_strength)
	# publisher.cmd(command)
	commandsFile.write(host + ' ' + command + "\n")

print 'instructing subscribers'
for host in subscribers:
	# subscriber = net.get(host)
	topic = random.sample(topics,1)
	print 'adding subscribercommand with topic {}'.format(topic)
	command = "python {}/s1.py {} {} &".format(proj_path,es_address,topic)
	# subscriber.cmd(command)
	commandsFile.write(host + ' ' + command + "\n")

commandsFile.close()

CLI (net)
