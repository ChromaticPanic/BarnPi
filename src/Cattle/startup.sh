#!/bin/bash
echo "Starting Cattle"


# get ether mac address
# ETHER_MAC=$(ip link | grep ether | tr -d ":" | awk '{print $2}' | sed '1p;d')
ETHER_MAC=$(cat /sys/class/net/eth0/address | tr -d ":")
UNIQUE_HOSTNAME="COW"$ETHER_MAC

echo "Ether MAC: $ETHER_MAC"
echo "Unique Hostname: $UNIQUE_HOSTNAME"


CURRENT_HOSTNAME=$(cat /proc/sys/kernel/hostname)

# set hostname
echo "$UNIQUE_HOSTNAME" > "/etc/hostname"

# set hostname in /etc/hosts
sed  "s/127.0.1.1.*$CURRENT_HOSTNAME/127.0.1.1\t$UNIQUE_HOSTNAME/g" /etc/hosts

service avaahi-daemon restart

CURRENT_HOSTNAME=$(cat /proc/sys/kernel/hostname)
echo "mdns hostname: $CURRENT_HOSTNAME"