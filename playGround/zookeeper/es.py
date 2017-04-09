from kazoo.client import KazooClient
import logging
logging.basicConfig()

# https://kazoo.readthedocs.io/en/latest/basic_usage.html
zk = KazooClient(hosts='localhost:2181')
zk.start()

def my_listener(state):
    if state == KazooState.LOST:
        # Register somewhere that the session was lost
        print('kazoo lost')
        pass
    elif state == KazooState.SUSPENDED:
        # Handle being disconnected from Zookeeper
        print('kazoo suspended')
        pass
    else:
        # Handle being connected/reconnected to Zookeeper
        pass
@zk.DataWatch('/es1')
def my_func(data, stat):
    print("Data is %s" % data)
    print("Version is %s" % stat.version)

@zk.ChildrenWatch('/es1')
def my_func(children):
    print "Children are %s" % children

zk.add_listener(my_listener)
# zk.create("/es1", b"a value")
raw_input('enter to close the process')
