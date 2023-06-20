from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, Controller
from mininet.link import TCLink
from mininet.wifi.node import Station, AccessPoint
from mininet.wifi.cli import CLI_wifi

def create_wifi_network():
    net = Mininet(topo=None, build=False)

    c1 = net.addController(name='c1', controller=Controller)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    ap1 = net.addAccessPoint('ap1', ssid='my-ssid', mode='g', channel='1', position='50,50,0')
    sta1 = net.addStation('sta1')
    sta2 = net.addStation('sta2')

    net.addLink(sta1, ap1)
    net.addLink(sta2, ap1)

    net.addLink(ap1, s1)
    net.addLink(s1, c1)

    net.build()

    c1.start()

    s1.start([c1])
    ap1.start([c1])

    sta1.cmd('ifconfig sta1-wlan0 up')
    sta2.cmd('ifconfig sta2-wlan0 up')
    sta1.cmd('ifconfig sta1-wlan0 192.168.0.1/24')
    sta2.cmd('ifconfig sta2-wlan0 192.168.0.2/24')

    sta1.cmd('ip route add default via 192.168.0.1')
    sta2.cmd('ip route add default via 192.168.0.1')

    CLI_wifi(net)

    net.stop()

if __name__ == '__main__':
    create_wifi_network()

