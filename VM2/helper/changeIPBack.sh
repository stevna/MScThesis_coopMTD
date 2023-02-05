sudo sed -i 's/192.168.1.29/192.168.1.23/g' /etc/dhcpcd.conf
sudo ifconfig eth0 down && sudo ifconfig eth0 up
