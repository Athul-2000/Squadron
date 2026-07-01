# Stop Dependent Processes

sudo pkill wpa_supplicant
sudo pkill dhclient
sudo pkill iperf3

# Delete existing namespaces
ip netns list
sudo ip netns del ns1
sudo ip netns del ns2


# Reload WiFi Driver
sudo modprobe -r rtw88_8812au
sudo modprobe rtw88_8812au


# Check WiFI Adapters are available
ip link
iw dev


# unblock RFkill, make blocked as 'No"
rfkill list
rfkill unblock all


# make Interfaces UP
sudo ip link set <iface> up

# Connect to WiFi
sudo wpa_supplicant -B -i <iface> -c ~/Squadron/wpa.conf

# Get IPv4 from DHCP
sudo dhclient <iface>
Verify:
Bash
iw dev <iface> link
ping -c 10 192.168.1.1
If latency is still hundreds of milliseconds here, stop and investigate that first. There's no point adding namespaces until a basic Wi-Fi connection behaves normally.
6. If basic Wi-Fi works, create namespaces again
Bash
sudo ip netns add ns1
sudo ip netns add ns2
Find the PHYs:
Bash
iw dev
Example:
Plain text
phy#0 -> wlx00c0caba4552
phy#1 -> wlx00c0caba4553
Move them:
Bash
sudo iw phy phy0 set netns name ns1
sudo iw phy phy1 set netns name ns2
Bring them up:
Bash
sudo ip netns exec ns1 ip link set lo up
sudo ip netns exec ns1 ip link set <iface1> up

sudo ip netns exec ns2 ip link set lo up
sudo ip netns exec ns2 ip link set <iface2> up
Then start wpa_supplicant inside each namespace.
Before rebuilding the namespace setup, I'd strongly recommend trying one dongle on the 5 GHz SSID and checking:
Bash
ping -c 20 192.168.1.1


Because your earlier

 results (0.2–0.4 Mbps and multi-second pings) suggest there may be a more fundamental AP/driver issue that should be resolved first.





Great. Assuming:
ns1 exists
The Wi-Fi interface is visible inside ns1
The interface is UP
First verify the interface name:
Bash
sudo ip netns exec ns1 iw dev
Suppose it shows:
Plain text
Interface wlx00c0caba4552
1. Bring up loopback and Wi-Fi interface
Bash
sudo ip netns exec ns1 ip link set lo up
sudo ip netns exec ns1 ip link set wlx00c0caba4552 up
2. Start wpa_supplicant inside the namespace
Bash
sudo ip netns exec ns1 wpa_supplicant -B \
    -i wlx00c0caba4552 \
    -c ~/Squadron/wpa.conf
If ~ doesn't work inside the namespace command, use the full path:
Bash
sudo ip netns exec ns1 wpa_supplicant -B \
    -i wlx00c0caba4552 \
    -c /home/squadron/Squadron/wpa.conf
3. Verify association
Wait a few seconds, then:
Bash
sudo ip netns exec ns1 iw dev wlx00c0caba4552 link
You should see:
Plain text
Connected to xx:xx:xx:xx:xx:xx
SSID: <your_ssid>
freq: 5180
(or 2412 if connected to 2.4 GHz)
4. Obtain an IP address
Bash
sudo ip netns exec ns1 dhclient wlx00c0caba4552
5. Verify IP
Bash
sudo ip netns exec ns1 ip addr show wlx00c0caba4552
6. Test connectivity
Bash
sudo ip netns exec ns1 ping -c 5 192.168.1.1
If any step fails, paste the output of:
Bash
sudo ip netns exec ns1 iw dev
sudo ip netns exec ns1 ip link
and the exact wpa_supplicant error.




sudo apt install python3-pyroute2

