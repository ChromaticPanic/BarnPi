# BarnPi

Information

Main switch (24-Port Gigabit GREENnet Switch - TRENDnet TEG-S24g) 
smaller switch (8-Port Gigabit GREENnet Switch - TRENDnet TEG-S80g).

The Raspberry Pi Model: Pi 4 8GB Starter Kit - 32GB (https://www.canakit.com/raspberry-pi-4-starter-kit.html)

 We do not have a preferred OS. As long it is one of the most recent and works well for the whole system. Talking about the PIs, since they are all plugged into power sources and connected to a switch using CAT6 cables, would it be possible to initialize them without physically accessing the SSD cards? We can manage to get the SSD cards down, but it would be nice if there was an option that did not require that to happen. 

The camera model is Vzense DCAM710 (their Github: https://github.com/Vzense)

For the contact method, email is the preferred method. 

We are in the process of purchasing the computer. Rest assured that the right permissions will be in place to allow software installation. For project documentation, we would prefer something a bit more old-school. GitHub is a bit foreign for the people who will be using the setup afterwards. Ideally, we are looking for text documents that explain the setup in detail (understandable for a layperson).

As for the requirements, we are mainly looking for:

    Initialize all 70 Raspberry PIs
    Set up the closed network of PIs so we can monitor and obtain data from the cameras attached to the PIs
    Prepare documentation explaining the setup and how to use it for future data collection periods.


In this position, you will be paid hourly and you will need to submit weekly timesheets (more information on that to come). Please keep consistent track of the hours you spend working on it.

Previous Work
tested using vzense, raspbian, rpi in lab , check it out.
password
camera resolutions, unable to use highest resolution
power adapter, error persists, could be software issue
camera lockout possible . needing physical reconnection

Potential issues with usbcable length

Network

gmail acct


Main
Initial
etckeeper
ansible
docker
tuptime
fail2ban


ssh create key pair
ssh copy key
ssh
ansible ping
ansible set timezone
install avahi-utils

cron job pull rsync

storage


Notification 
- gmail
- apprise
- awx

prometheus
grafana

Rpi
Initial

passwordless sudo
create a drive in ram for picture temp storage
install avahi-daemon
dynamically set hostname on boot to RPIaxaxaxax mac address
sudo hostname rpiaxaxaxax
sudo service avahi-daemon restart
ssh pubkey auth


node exporter
cpu
ram
uptime

test
