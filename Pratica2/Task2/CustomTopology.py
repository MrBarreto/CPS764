from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import RemoteController,OVSSwitch
from mininet.cli import CLI


class CustomTopology(Topo):
    "A custom topology with 4 swittches and 7 hosts"
    def build(self):
        switch1 = self.addSwitch(f's1', cls=OVSSwitch, protocols='OpenFlow13')
        switch2 = self.addSwitch(f's2', cls=OVSSwitch, protocols='OpenFlow13')
        switch3 = self.addSwitch(f's3', cls=OVSSwitch, protocols='OpenFlow13')
        switch1 = self.addSwitch(f's4', cls=OVSSwitch, protocols='OpenFlow13')
        self.addLink('s1','s2')
        self.addLink('s2','s3')
        self.addLink('s3','s4')
        host = self.addHost(f'h1')
        host = self.addHost(f'h2')
        host = self.addHost(f'h3')
        host = self.addHost(f'h4')
        host = self.addHost(f'h5')
        host = self.addHost(f'h6')
        host = self.addHost(f'h7')
        self.addLink('h1','s1')
        self.addLink('h2','s1')
        self.addLink('h3','s1')
        self.addLink('h4','s2')
        self.addLink('h5','s2')
        self.addLink('h6','s4')
        self.addLink('h7','s4')