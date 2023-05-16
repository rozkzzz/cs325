#!/usr/bin/env python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='192.168.0.0/24')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, failMode='standalone')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='192.168.0.101', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='192.168.0.102', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='192.168.0.103', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='192.168.0.104', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='192.168.0.105', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='192.168.0.106', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='192.168.0.107', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='192.168.0.108', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='192.168.0.109', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='192.168.0.110', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='192.168.0.111', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='192.168.0.112', defaultRoute=None)
    h13 = net.addHost('h13', cls=Host, ip='192.168.0.113', defaultRoute=None)

    info( '*** Add links\n')
    net.addLink(s1, s2)
    net.addLink(s2, h1)
    net.addLink(s2, h2)
    net.addLink(s2, h3)
    net.addLink(s2, s3)
    net.addLink(s3, h4)
    net.addLink(s3, h5)
    net.addLink(s3, h6)
    net.addLink(s1, s4)
    net.addLink(s4, h7)
    net.addLink(s4, h8)
    net.addLink(s4, h9)
    net.addLink(s1, s5)
    net.addLink(s5, h10)
    net.addLink(s5, h11)
    net.addLink(s5, h12)
    net.addLink(s5, h13)

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s1').start([])
    net.get('s2').start([])
    net.get('s3').start([])
    net.get('s4').start([])
    net.get('s5').start([])

    info( '*** Post configure switches and hosts\n')
    #s2
    call("ovs-vsctl set port s2-eth2 tag=100",shell=True)
    call("ovs-vsctl set port s2-eth3 tag=200",shell=True)
    call("ovs-vsctl set port s2-eth4 tag=100",shell=True)
    call("ovs-vsctl set port s2-eth5 trunks=100,200,300",shell=True)
    #s3
    call("ovs-vsctl set port s3-eth2 tag=200",shell=True)
    call("ovs-vsctl set port s3-eth3 tag=100",shell=True)
    call("ovs-vsctl set port s3-eth4 tag=300",shell=True)
    call("ovs-vsctl set port s3-eth1 trunks=100,200,300",shell=True)
    #s1
    call("ovs-vsctl set port s1-eth1 trunks=100,200,300",shell=True)
    call("ovs-vsctl set port s1-eth2 trunks=100,200,300",shell=True)
    call("ovs-vsctl set port s1-eth3 trunks=100,200,300",shell=True)
    #s4
    call("ovs-vsctl set port s4-eth2 tag=100",shell=True)
    call("ovs-vsctl set port s4-eth3 tag=200",shell=True)
    call("ovs-vsctl set port s4-eth4 tag=300",shell=True)
    call("ovs-vsctl set port s4-eth1 trunks=100,200,300",shell=True)
    #s5
    call("ovs-vsctl set port s5-eth2 tag=300",shell=True)
    call("ovs-vsctl set port s5-eth3 tag=100",shell=True)
    call("ovs-vsctl set port s5-eth4 tag=200",shell=True)
    call("ovs-vsctl set port s5-eth1 trunks=100,200,300",shell=True)
    call("ovs-vsctl set port s5-eth5 tag=300",shell=True)
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()

