# BarnPi

Commands

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/check_cam.yaml | tee check_cam.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/check_cam_retry.yaml | tee retry.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/fetch_captured_frames.yaml | tee fetch_captured_frames.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/capture_frames.yaml | tee capture_frames.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/clear_ram_disk.yaml | tee clear_ram_disk.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/push_project_to_hosts.yaml | tee push_project_to_hosts.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/reboot_swarm.yaml | tee reboot_swarm.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/sync_to_public.yaml | tee sync_to_public.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/sync_to_nas.yaml | tee sync_to_nas.txt

time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/usb_power_cycle.yaml | tee usb_power_cycle.txt

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
- [ ] Main computer will push any updates of collection interval to the RPIs

- [ ] RPIs will collect images at specified intervals and keep locally until transfers are completed and verified
- [x] RPI will report system health to main computer

- [ ] NAS will fill up one system at a time
- [x] NAS should have some redundancy for drive failure risks
- [x] Images will likely be stored in separate folders for each pi. file names will contain the RPI unique identifier, timestamp, and maybe other relevant information like resolution

USB length limit for the camera to work is 4 meters
- tested with 3m extension + 1m camera cable
- tested with 4.5m extension + 1m camera cable
- tested with 3m + 4.5m extension + 1m camera cable
With longer cables the camera light turns on but the camera is not detected by the system. This is a physics issue with digital signals over copper cables. There is a voltage drop over long cables preventing communication.


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
