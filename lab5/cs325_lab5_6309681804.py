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
                   ipBase='10.10.10.0/24')

    info( '*** Adding controller\n' )
    info( '*** Add switches\n')
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch, failMode='standalone')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch, failMode='standalone')
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch, failMode='standalone')
    s4 = net.addSwitch('s4', cls=OVSKernelSwitch, failMode='standalone')
    s5 = net.addSwitch('s5', cls=OVSKernelSwitch, failMode='standalone')


    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='no ip defined/8', defaultRoute=None)
    h13 = net.addHost('h13', cls=Host, ip='no ip defined/8', defaultRoute=None)
	
    r1 = net.addHost('r1', cls=Node, ip='10.10.10.2/24')
    nat = net.addNAT('nat',ip='10.10.10.1/24').configDefault()
    
    info( '*** Add links\n')
    net.addLink(s1, r1)
    net.addLink(r1, s2)
    net.addLink(r1, s4)
    net.addLink(r1, s5)
    net.addLink(s2, s3)
    net.addLink(s2, s4)
    net.addLink(s4, s5)
    net.addLink(s2, h1)
    net.addLink(s2, h2)
    net.addLink(s2, h3)
    net.addLink(s3, h4)
    net.addLink(s3, h5)
    net.addLink(s3, h6)
    net.addLink(s4, h7)
    net.addLink(s4, h8)
    net.addLink(s4, h9)
    net.addLink(s5, h10)
    net.addLink(s5, h11)
    net.addLink(s5, h12)
    net.addLink(s5, h13)

    
    dhcp1 = net.addHost('dhcp1',ip='192.168.10.2/24')
    dhcp2 = net.addHost('dhcp2',ip='192.168.20.2/24')
    dhcp3 = net.addHost('dhcp3',ip='192.168.30.2/24')
    
    net.addLink(s4, dhcp1)
    net.addLink(s5, dhcp2)
    net.addLink(s3, dhcp3)
    
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
    call(" ovs-ofctl add-flow s1 action=normal",shell=True)
    call(" ovs-ofctl add-flow s2 action=normal",shell=True)
    call(" ovs-ofctl add-flow s3 action=normal",shell=True)
    call(" ovs-ofctl add-flow s4 action=normal",shell=True)
    call(" ovs-ofctl add-flow s5 action=normal",shell=True)
    #s1
    r1.cmd("ovs-vsctl set port r1-eth0 tag=400")
    #s2
    call("ovs-vsctl set port s2-eth4 tag=100",shell=True)
    call("ovs-vsctl set port s2-eth5 tag=200",shell=True)
    call("ovs-vsctl set port s2-eth6 tag=100",shell=True)
    call("ovs-vsctl set port s2-eth1 tag=100",shell=True)
    #s3
    call("ovs-vsctl set port s3-eth2 tag=200",shell=True)
    call("ovs-vsctl set port s3-eth3 tag=100",shell=True)
    call("ovs-vsctl set port s3-eth4 tag=300",shell=True)
    #s4
    call("ovs-vsctl set port s4-eth4 tag=100",shell=True)
    call("ovs-vsctl set port s4-eth5 tag=200",shell=True)
    call("ovs-vsctl set port s4-eth6 tag=300",shell=True)
    call("ovs-vsctl set port s4-eth1 tag=200",shell=True)
    #s5
    call("ovs-vsctl set port s5-eth3 tag=300",shell=True)
    call("ovs-vsctl set port s5-eth4 tag=100",shell=True)
    call("ovs-vsctl set port s5-eth5 tag=200",shell=True)
    call("ovs-vsctl set port s5-eth6 tag=300",shell=True)
    call("ovs-vsctl set port s5-eth1 tag=300",shell=True)
    #trunk
    call("ovs-vsctl set port s2-eth2 trunks=100,200,300",shell=True)#s2->s3
    call("ovs-vsctl set port s3-eth1 trunks=100,200,300",shell=True)#s3->s2
    
    call("ovs-vsctl set port s2-eth3 trunks=100,200,300",shell=True)#s2->s4
    call("ovs-vsctl set port s4-eth2 trunks=100,200,300",shell=True)#s4->s2
    
    call("ovs-vsctl set port s4-eth3 trunks=100,200,300",shell=True)#s4->s5
    call("ovs-vsctl set port s5-eth2 trunks=100,200,300",shell=True)#s5->s4
    
    #dhcp
    call("ovs-vsctl set port s4-eth7 tag=100",shell=True)
    call("ovs-vsctl set port s5-eth7 tag=200",shell=True)
    call("ovs-vsctl set port s3-eth5 tag=300",shell=True)
    
    dhcp1.cmd("dhcpd -cf /etc/dhcp/dhcpd1.conf --no-pid")
    dhcp2.cmd("dhcpd -cf /etc/dhcp/dhcpd2.conf --no-pid")
    dhcp3.cmd("dhcpd -cf /etc/dhcp/dhcpd3.conf --no-pid")
    #config
    r1.cmd("route add default gw 10.10.10.1 r1-eth0")
    r1.cmd("ip addr add 192.168.10.1/24 dev r1-eth1")
    r1.cmd("ip addr add 192.168.20.1/24 dev r1-eth2")
    r1.cmd("ip addr add 192.168.30.1/24 dev r1-eth3")

    call("sysctl -w net.ipv4.ip_forward=1",shell=True)
    h1.cmd("dhclient")
    h2.cmd("dhclient")
    h3.cmd("dhclient")
    h4.cmd("dhclient")
    h5.cmd("dhclient")
    h6.cmd("dhclient")
    h7.cmd("dhclient")
    h8.cmd("dhclient")
    h9.cmd("dhclient")
    h10.cmd("dhclient")
    h11.cmd("dhclient")
    h12.cmd("dhclient")
    h13.cmd("dhclient")
    r1.cmd("iptables -t nat -A POSTROUTING -o r1-eth0 -j MASQUERADE")
    
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()
