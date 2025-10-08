from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController,OVSSwitch
import queue

class SingleSwitchTopo(Topo):
    "Single switch connected to n hosts."
    def build(self, n=2):
        switch = self.addSwitch('s1', cls=OVSSwitch, protocols='OpenFlow13')
        for h in range(n):
            host = self.addHost(f'h{h+1}')
            self.addLink(host, switch)

class LinearTopo(Topo):
    "A single host connected to a switch"
    def build(self, n=2):
        for h in range(n):
            switch = self.addSwitch(f's{h+1}', cls=OVSSwitch, protocols='OpenFlow13')
            host = self.addHost(f'h{h+1}')
            self.addLink(host, switch)
            if h > 0:
                self.addLink(f's{h}', f's{h+1}')

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

def simpleTest(topo):
    "Create and test a simple network"
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
    selected = False
    while not selected:
        try:
            topologia = int(input("Selecione\n1 - Topologia Single\n2 - Topologia Linear\n3 - Topologia em árvore"))
        except ValueError:
            print("Erro: A entrada não é um número válido. Por favor, digite 1, 2 ou 3.")
            next
        
        if topologia == 1:
            selected = True
            size = int(input("Digite o número de hosts: "))
            topo = SingleSwitchTopo(n=size)
        
        elif topologia == 2:
            selected = True
            size = int(input("Digite o número de hosts: "))
            topo = LinearTopo(n=size)
        
        elif topologia == 3:
            selected = True
            depth = int(input("Digite a profundidade da árvore: "))
            fanout = int(input("Digite o fanout da árvore: "))
            topo = TreeTopo(depth=depth, fanout=fanout)

        else:
            print("Digite um número válido")

    simpleTest(topo)