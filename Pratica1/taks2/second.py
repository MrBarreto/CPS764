from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController,OVSSwitch


class LinearTopo(Topo):
    "A single host connected to a switch"
    def build(self, n=2):
        for h in range(n):
            switch = self.addSwitch(f's{h+1}', cls=OVSSwitch, protocols='OpenFlow13')
            host = self.addHost(f'h{h+1}')
            self.addLink(host, switch)
            if h > 0:
                self.addLink(f's{h}', f's{h+1}')

def simpleTest():
    "Create and test a simple network"
    topo = LinearTopo(n=10)
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

