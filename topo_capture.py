from mininet.net import Mininet
from mininet.topo import SingleSwitchTopo
from mininet.node import OVSBridge
from mininet.log import setLogLevel
import time

setLogLevel('info')
net = Mininet(topo=SingleSwitchTopo(3), switch=OVSBridge, controller=None)
net.start()
h1, h2, h3 = net.get('h1', 'h2', 'h3')
net.pingAll()

h2.cmd('iperf3 -s -D')
time.sleep(1)

def run(name, client_cmd):
    h2.cmd(f'tcpdump -s 96 -i h2-eth0 -w {name}.pcap &')
    time.sleep(2)
    h1.cmd(f'{client_cmd} > {name}.log')
    time.sleep(2)
    h2.cmd('pkill tcpdump')
    time.sleep(1)

run('tcp',  'iperf3 -c 10.0.0.2 -b 100M -t 10')
run('udp',  'iperf3 -c 10.0.0.2 -u -b 5M -t 10')
run('icmp', 'ping -c 20 10.0.0.2')

h2.cmd('pkill iperf3')
net.stop()
