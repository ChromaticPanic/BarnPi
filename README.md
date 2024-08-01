# BarnPi

# System Overview
The BarnPi system is a network of Raspberry Pi computers that are used to capture images from cameras attached to the Raspberry Pi. The images are stored on a network-attached storage (NAS) device for later analysis. The system is designed to be used in a barn environment to monitor the health and behavior of livestock.

The system consists of three main components:
- The main computer, which is responsible for monitoring the Raspberry Pi computers and managing the NAS device.
- The Raspberry Pi computers, which capture images from the cameras and store them locally until they can be transferred to the NAS device.
- The NAS devices, which stores the images captured by the Raspberry Pi computers.

The main computer sits between 2 networks, the University network and the BarnPi network. The University network is used for remote access to the main computer, while the BarnPi network is used for communication between the main computer, the Raspberry Pi computers, and the pi

# Main Computer


# Raspberry Pi Computers


# NAS Devices


# Code Overview
All the code for the BarnPi system is stored in the `src` directory. The code is organized into several subdirectories, each of which contains code for a specific component of the system.

## DCAM
The `DCAM` directory contains code for capturing images from the cameras attached to the Raspberry Pi computers. The code is written in Python and uses the `vzense` library to interface with the cameras.

## Cattle
The `Cattle` directory contains code needed by the raspberry pi computer OS to function properly. This includes the startup script and the systemd service file. Which assigns a unique hostname to each Raspberry Pi computer based on its MAC address.

## Rancher
The `Rancher` directory contains code for managing the Raspberry Pi computers and the NAS devices. This includes Ansible playbooks for deploying code to the Raspberry Pi computers, managing the NAS devices, and performing other administrative tasks.



Onboarding
Step 1: install vscode
Step 2: Desktop\Projects
Step 3: launch VScode Project
Step 4: BarnPi/src/DCAM/capture_config.ini

tar netcat

Commands

Shell wrappers

Ansible
time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/check_cam.yaml | tee /home/rancher/Project/BarnPi/log/check_cam.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/check_cam_retry.yaml | tee /home/rancher/Project/BarnPi/log/retry.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/fetch_captured_frames.yaml | tee /home/rancher/Project/BarnPi/log/fetch_captured_frames.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/capture_frames.yaml | tee /home/rancher/Project/BarnPi/log/capture_frames.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/clear_ram_disk.yaml | tee /home/rancher/Project/BarnPi/log/clear_ram_disk.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/push_project_to_hosts.yaml | tee /home/rancher/Project/BarnPi/log/push_project_to_hosts.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/reboot_swarm.yaml | tee /home/rancher/Project/BarnPi/log/reboot_swarm.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/sync_to_public.yaml | tee /home/rancher/Project/BarnPi/log/sync_to_public.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/sync_to_nas.yaml | tee /home/rancher/Project/BarnPi/log/sync_to_nas.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/usb_power_cycle.yaml | tee /home/rancher/Project/BarnPi/log/usb_power_cycle.txt

Bash


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


- [x] Main computer is in charge of monitoring all the pi's
- [ ] Main computer is in charge of managing the NAS boxes (which one is active)
- [ ] Main computer is in charge of initiating file transfers from the pi's to the NAS
- [ ] Main computer should notify (likely via email) if RPI or camera issues detected
- [ ] Main computer should notify (likely via email) when NAS is nearing capacity
- [ ] If the main computer can detect NAS issues then it will also notify for those. (e.g. drive failure needing replacement and resilvering)
- [x] Main computer will push any updates of collection interval to the RPIs

- [x] RPIs will collect images at specified intervals and keep locally until transfers are completed and verified
- [x] RPI will report system health to main computer

- [x] NAS will fill up one system at a time
- [ ] NAS should have some redundancy for drive failure risks Raid 5 1gbps Raid 10 2gbps
- [x] Images will likely be stored in separate folders for each pi. file names will contain the RPI unique identifier, timestamp, and maybe other relevant information like resolution

USB length limit for the camera to work is 4 meters
- tested with 3m extension + 1m camera cable
- tested with 4.5m extension + 1m camera cable
- tested with 3m + 4.5m extension + 1m camera cable
With longer cables the camera light turns on but the camera is not detected by the system. This is a physics issue with digital signals over copper cables. There is a voltage drop over long cables preventing communication.

NAS Config
animalscienceadmin
cowmain

Raid 5 BTRFS Theoretical 1gbps write speed
Port 1 DHCP
Port 2 Static 192.168.50.10, 192.168.50.20

shared folder /volume1/barndata

home folder /volume1/homes/cowmain

recv /var/packages/DiagnosisTool/target/tool/ncat -l -p 7000 | pv | tar -xpf -
send tar -cf - * | pv | nc destinationHost 7000

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
