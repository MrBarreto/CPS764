from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController,OVSSwitch
import queue

class TreeTopo(Topo):
    "Switches connected in a tree topology"
    def build(self, depth=2, fanout=2):
        queueNode = queue.Queue()
        rootName = 's1'
        self.addSwitch(rootName, cls=OVSSwitch, protocols='OpenFlow13')
        queueNode.put((rootName, 1))
        nodeId = 2

        while not queueNode.empty():
            parentName, parentLevel = queueNode.get()
            if parentLevel <= depth:
                isHost = (parentLevel == depth)
                
                for i in range(fanout):
                    if isHost:
                        childType = 'h'
                        childName = f'{childType}{nodeId}'
                        self.addHost(childName)
                    else:
                        childType = 's'
                        childName = f'{childType}{nodeId}'
                        self.addSwitch(childName, cls=OVSSwitch, protocols='OpenFlow13')
                        queueNode.put((childName, parentLevel + 1))
                    
                    self.addLink(parentName, childName)
                    nodeId += 1
                
def simpleTest():
    "Create and test a simple network"
    topo = TreeTopo(depth=3, fanout=2)
    net = Mininet(topo, controller=None)
    net.addController( 'c0', controller=RemoteController, ip='192.168.123.1', port=6653)
    net.start()
    print( "Dumping host connections" )
    dumpNodeConnections(net.hosts)
    print( "Testing network connectivity" )
    net.pingAll()
    net.stop()

if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()

