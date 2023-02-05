sudo sed -i 's/192.168.1.27/192.168.1.27/g' /etc/dhcpcd.conf
sudo ifconfig eth0 down && sudo ifconfig eth0 up
