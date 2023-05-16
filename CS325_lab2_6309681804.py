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
    h1 = net.addHost('h1', cls=Host, ip='192.168.0.101', mac='00:00:00:00:00:01', defaultRoute=None)
    h2 = net.addHost('h2', cls=Host, ip='192.168.0.102', mac='00:00:00:00:00:02', defaultRoute=None)
    h3 = net.addHost('h3', cls=Host, ip='192.168.0.103', mac='00:00:00:00:00:03', defaultRoute=None)
    h4 = net.addHost('h4', cls=Host, ip='192.168.0.104', mac='00:00:00:00:00:04', defaultRoute=None)
    h5 = net.addHost('h5', cls=Host, ip='192.168.0.105', mac='00:00:00:00:00:05', defaultRoute=None)
    h6 = net.addHost('h6', cls=Host, ip='192.168.0.106', mac='00:00:00:00:00:06', defaultRoute=None)
    h7 = net.addHost('h7', cls=Host, ip='192.168.0.107', mac='00:00:00:00:00:07', defaultRoute=None)
    h8 = net.addHost('h8', cls=Host, ip='192.168.0.108', mac='00:00:00:00:00:08', defaultRoute=None)
    h9 = net.addHost('h9', cls=Host, ip='192.168.0.109', mac='00:00:00:00:00:09', defaultRoute=None)
    h10 = net.addHost('h10', cls=Host, ip='192.168.0.110', mac='00:00:00:00:00:10', defaultRoute=None)
    h11 = net.addHost('h11', cls=Host, ip='192.168.0.111', mac='00:00:00:00:00:11', defaultRoute=None)
    h12 = net.addHost('h12', cls=Host, ip='192.168.0.112', mac='00:00:00:00:00:12', defaultRoute=None)
    h13 = net.addHost('h13', cls=Host, ip='192.168.0.113', mac='00:00:00:00:00:13', defaultRoute=None)

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
    net.start()
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

    call("ovs-ofctl del-flows s1",shell=True)
    call("ovs-ofctl del-flows s2",shell=True)
    call("ovs-ofctl del-flows s3",shell=True)
    call("ovs-ofctl del-flows s4",shell=True)
    call("ovs-ofctl del-flows s5",shell=True)

    #s1
    for i in range(1,14):
        call(f"ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:{i:02},actions=output:1" if i<=6 else
            f"ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:{i:02},actions=output:2" if i<=9 else
            f"ovs-ofctl add-flow s1 dl_dst=00:00:00:00:00:{i:02},actions=output:3", shell=True)

    call("ovs-ofctl add-flow s1 dl_type=0x806,nw_proto=1,actions=output:1,2,3", shell=True)

    #s2
    call("ovs-ofctl add-flow s2 in_port=s2-eth1,dl_dst=00:00:00:00:00:01,actions=output:s2-eth2",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth1,dl_dst=00:00:00:00:00:02,actions=output:s2-eth3",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth1,dl_dst=00:00:00:00:00:03,actions=output:s2-eth4",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth1,dl_dst=00:00:00:00:00:04,actions=output:s2-eth5",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth1,dl_dst=00:00:00:00:00:05,actions=output:s2-eth5",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth1,dl_dst=00:00:00:00:00:06,actions=output:s2-eth5",shell=True)
    
    call("ovs-ofctl add-flow s2 in_port=s2-eth2,dl_dst=00:00:00:00:00:03,actions=output:s2-eth4",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth2,dl_dst=00:00:00:00:00:05,actions=output:s2-eth5",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth2,dl_dst=00:00:00:00:00:07,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth2,dl_dst=00:00:00:00:00:11,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth3,dl_dst=00:00:00:00:00:04,actions=output:s2-eth5",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth3,dl_dst=00:00:00:00:00:08,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth3,dl_dst=00:00:00:00:00:12,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth4,dl_dst=00:00:00:00:00:01,actions=output:s2-eth2",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth4,dl_dst=00:00:00:00:00:05,actions=output:s2-eth5",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth4,dl_dst=00:00:00:00:00:07,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth4,dl_dst=00:00:00:00:00:11,actions=output:s2-eth1",shell=True)

    call("ovs-ofctl add-flow s2 in_port=s2-eth5,dl_dst=00:00:00:00:00:01,actions=output:s2-eth2",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth5,dl_dst=00:00:00:00:00:02,actions=output:s2-eth3",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth5,dl_dst=00:00:00:00:00:03,actions=output:s2-eth4",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth5,dl_dst=00:00:00:00:00:07,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth5,dl_dst=00:00:00:00:00:08,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth5,dl_dst=00:00:00:00:00:09,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth5,dl_dst=00:00:00:00:00:10,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth5,dl_dst=00:00:00:00:00:11,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth5,dl_dst=00:00:00:00:00:12,actions=output:s2-eth1",shell=True)
    call("ovs-ofctl add-flow s2 in_port=s2-eth5,dl_dst=00:00:00:00:00:13,actions=output:s2-eth1",shell=True)
    
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:01,nw_proto=1,actions=output:1,2,4,5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:02,nw_proto=1,actions=output:1,3,5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:03,nw_proto=1,actions=output:1,2,4,5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:04,nw_proto=1,actions=output:1,3,5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:05,nw_proto=1,actions=output:1,2,4,5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:06,nw_proto=1,actions=output:1,5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:07,nw_proto=1,actions=output:2,4,5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:08,nw_proto=1,actions=output:3,5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:09,nw_proto=1,actions=output:5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:10,nw_proto=1,actions=output:5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:11,nw_proto=1,actions=output:2,4,5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:12,nw_proto=1,actions=output:3,5",shell=True)
    call("ovs-ofctl add-flow s2 dl_type=0x806,dl_src=00:00:00:00:00:13,nw_proto=1,actions=output:5",shell=True)

    #s3
    call("ovs-ofctl add-flow s3 in_port=s3-eth1,dl_dst=00:00:00:00:00:04,actions=output:s3-eth2",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth1,dl_dst=00:00:00:00:00:05,actions=output:s3-eth3",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth1,dl_dst=00:00:00:00:00:06,actions=output:s3-eth4",shell=True)

    call("ovs-ofctl add-flow s3 in_port=s3-eth2,dl_dst=00:00:00:00:00:02,actions=output:s3-eth1",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth2,dl_dst=00:00:00:00:00:08,actions=output:s3-eth1",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth2,dl_dst=00:00:00:00:00:12,actions=output:s3-eth1",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth3,dl_dst=00:00:00:00:00:01,actions=output:s3-eth1",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth3,dl_dst=00:00:00:00:00:03,actions=output:s3-eth1",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth3,dl_dst=00:00:00:00:00:07,actions=output:s3-eth1",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth3,dl_dst=00:00:00:00:00:11,actions=output:s3-eth1",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth4,dl_dst=00:00:00:00:00:09,actions=output:s3-eth1",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth4,dl_dst=00:00:00:00:00:10,actions=output:s3-eth1",shell=True)
    call("ovs-ofctl add-flow s3 in_port=s3-eth4,dl_dst=00:00:00:00:00:13,actions=output:s3-eth1",shell=True)

    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:01,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:02,nw_proto=1,actions=output:1,2",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:03,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:04,nw_proto=1,actions=output:1,2",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:05,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:06,nw_proto=1,actions=output:1,4",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:07,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:08,nw_proto=1,actions=output:1,2",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:09,nw_proto=1,actions=output:1,4",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:10,nw_proto=1,actions=output:1,4",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:11,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:12,nw_proto=1,actions=output:1,2",shell=True)
    call("ovs-ofctl add-flow s3 dl_type=0x806,dl_src=00:00:00:00:00:13,nw_proto=1,actions=output:1,4",shell=True)

    #s4
    call("ovs-ofctl add-flow s4 in_port=s4-eth1,dl_dst=00:00:00:00:00:07,actions=output:s4-eth2",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth1,dl_dst=00:00:00:00:00:08,actions=output:s4-eth3",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth1,dl_dst=00:00:00:00:00:09,actions=output:s4-eth4",shell=True)

    call("ovs-ofctl add-flow s4 in_port=s4-eth2,dl_dst=00:00:00:00:00:01,actions=output:s4-eth1",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth2,dl_dst=00:00:00:00:00:03,actions=output:s4-eth1",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth2,dl_dst=00:00:00:00:00:05,actions=output:s4-eth1",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth2,dl_dst=00:00:00:00:00:11,actions=output:s4-eth1",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth3,dl_dst=00:00:00:00:00:02,actions=output:s4-eth1",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth3,dl_dst=00:00:00:00:00:04,actions=output:s4-eth1",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth3,dl_dst=00:00:00:00:00:12,actions=output:s4-eth1",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth4,dl_dst=00:00:00:00:00:06,actions=output:s4-eth1",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth4,dl_dst=00:00:00:00:00:10,actions=output:s4-eth1",shell=True)
    call("ovs-ofctl add-flow s4 in_port=s4-eth4,dl_dst=00:00:00:00:00:13,actions=output:s4-eth1",shell=True)

    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:01,nw_proto=1,actions=output:1,2",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:02,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:03,nw_proto=1,actions=output:1,2",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:04,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:05,nw_proto=1,actions=output:1,2",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:06,nw_proto=1,actions=output:1,4",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:07,nw_proto=1,actions=output:1,2",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:08,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:09,nw_proto=1,actions=output:1,4",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:10,nw_proto=1,actions=output:1,4",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:11,nw_proto=1,actions=output:1,2",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:12,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s4 dl_type=0x806,dl_src=00:00:00:00:00:13,nw_proto=1,actions=output:1,4",shell=True)
    #s5
    call("ovs-ofctl add-flow s5 in_port=1,dl_dst=00:00:00:00:00:10,actions=output:2",shell=True)
    call("ovs-ofctl add-flow s5 in_port=1,dl_dst=00:00:00:00:00:11,actions=output:3",shell=True)
    call("ovs-ofctl add-flow s5 in_port=1,dl_dst=00:00:00:00:00:12,actions=output:4",shell=True)
    call("ovs-ofctl add-flow s5 in_port=1,dl_dst=00:00:00:00:00:13,actions=output:5",shell=True)

    call("ovs-ofctl add-flow s5 in_port=s5-eth3,dl_dst=00:00:00:00:00:01,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth3,dl_dst=00:00:00:00:00:03,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth3,dl_dst=00:00:00:00:00:05,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth3,dl_dst=00:00:00:00:00:07,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth4,dl_dst=00:00:00:00:00:02,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth4,dl_dst=00:00:00:00:00:04,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth4,dl_dst=00:00:00:00:00:08,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth2,dl_dst=00:00:00:00:00:06,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth2,dl_dst=00:00:00:00:00:09,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth2,dl_dst=00:00:00:00:00:13,actions=output:s5-eth5",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth5,dl_dst=00:00:00:00:00:06,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth5,dl_dst=00:00:00:00:00:09,actions=output:s5-eth1",shell=True)
    call("ovs-ofctl add-flow s5 in_port=s5-eth5,dl_dst=00:00:00:00:00:10,actions=output:s5-eth2",shell=True)

    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:01,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:02,nw_proto=1,actions=output:1,4",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:03,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:04,nw_proto=1,actions=output:1,4",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:05,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:06,nw_proto=1,actions=output:1,2,5",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:07,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:08,nw_proto=1,actions=output:1,4",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:09,nw_proto=1,actions=output:1,2,5",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:10,nw_proto=1,actions=output:1,2,5",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:11,nw_proto=1,actions=output:1,3",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:12,nw_proto=1,actions=output:1,4",shell=True)
    call("ovs-ofctl add-flow s5 dl_type=0x806,dl_src=00:00:00:00:00:13,nw_proto=1,actions=output:1,2,5",shell=True)

    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()