#!/usr/bin/env python
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.nodelib import NAT
from mininet.node import Host, Node
from subprocess import call
def myNetwork():
	net = Mininet( topo=None,
		build=False,
		ipBase='192.168.0.0/24')
	info( '*** Add switches\n')
	s1 = net.addSwitch('s1')
	s2 = net.addSwitch('s2')
	s3 = net.addSwitch('s3')
	r1 = net.addHost('r1', cls=Node,ip='192.168.0.1/24')
	nat = net.addNAT('nat',ip='192.168.0.254/24').configDefault()
	info( '*** Add hosts\n')
	h1 = net.addHost('h1',ip='192.168.1.10/24')
	h2 = net.addHost('h2',ip='192.168.2.20/24')
	h3 = net.addHost('h3',ip='192.168.1.30/24')
	h4 = net.addHost('h4',ip='192.168.2.40/24')
	info( '*** Add links\n')
	net.addLink(s1, r1)
	net.addLink(s2, s3)
	net.addLink(s2, r1)
	net.addLink(s3, r1)
	net.addLink(s2, h1)
	net.addLink(s2, h2)
	net.addLink(s3, h3)
	net.addLink(s3, h4)
	info( '*** Starting network\n')
	

	
	net.start()
	r1.cmd("route add default gw 192.168.0.254 r1-eth0")
	call("ovs-ofctl add-flow s1 action=normal",shell=True)
	call("ovs-ofctl add-flow s2 action=normal",shell=True)
	call("ovs-ofctl add-flow s3 action=normal",shell=True)
	call("ovs-vsctl set port s2-eth1 trunks=10,20",shell=True)
	call("ovs-vsctl set port s3-eth1 trunks=10,20",shell=True)
	call("ovs-vsctl set port s2-eth2 tag=10",shell=True)
	call("ovs-vsctl set port s2-eth3 tag=10",shell=True)
	call("ovs-vsctl set port s2-eth4 tag=20",shell=True)
	call("ovs-vsctl set port s3-eth2 tag=20",shell=True)
	call("ovs-vsctl set port s3-eth3 tag=10",shell=True)
	call("ovs-vsctl set port s3-eth4 tag=20",shell=True)
	r1.cmd("ip addr add 192.168.1.1/24 dev r1-eth1",shell=True)
	r1.cmd("ip addr add 192.168.2.1/24 dev r1-eth2",shell=True)
	call("sysctl -w net.ipv4.ip_forward=1",shell=True)
	h1.cmd("route add default gw 192.168.1.1 h1-eth0",shell=True)
	h2.cmd("route add default gw 192.168.2.1 h2-eth0",shell=True)
	h3.cmd("route add default gw 192.168.1.1 h3-eth0",shell=True)
	h4.cmd("route add default gw 192.168.2.1 h4-eth0",shell=True)	
	
	CLI(net)
	net.stop()
if __name__ == '__main__':
	setLogLevel( 'info' )
	myNetwork()
