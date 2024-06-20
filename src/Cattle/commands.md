sudo apt update && sudo apt upgrade -y 
sudo shutdown -r now 

sudo apt install -y etckeeper
sudo apt install -y tuptime avahi-daemon v4l-utils python3.12-venv

sudo mkdir /mnt/ramdisk
sudo chown cowmain /mnt/ramdisk

v4l2-ctl --list-devices

mkdir project
cd project
git clone therepo
cd BarnPi

python -m venv src/DCAM

source bin/activate

pip install -r requirements.txt
python install.py

/set perms
sudo chmod 744 /home/cowmain/project/BarnPi/src/Cattle/cattle_startup.sh
sudo cp /home/cowmain/project/BarnPi/src/Cattle/startup.sh /usr/local/bin/cattle_startup.sh
sudo chmod 664 /home/cowmain/project/BarnPi/src/Cattle/cattle_startup.service
sudo cp /home/cowmain/project/BarnPi/src/Cattle/cattle_startup.service /etc/systemd/system/cattle_startup.service
sudo systemctl daemon-reload
sudo systemctl enable cattle_startup.service

reboot

hostname_YYYYMMDD_HHMMSS_channel

sudo netplan try --config-file /etc/netplan/50-cloud-init.yaml