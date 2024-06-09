sudo apt update && sudo apt upgrade -y 
sudo shutdown -r now 

sudo apt install etckeeper tuptime
mkdir project
git clone therepo

sudo apt install -y v4l-utils
v4l2-ctl --list-devices

sudo apt install -y python3.12-venv
python -m venv BarnPi/src/DCAM

source bin/activate
touch BarnPi/src/DCAM/requirements.txt
echo "numpy" > BarnPi/src/DCAM/requirements.txt
echo "opencv-python-headless" > BarnPi/src/DCAM/requirements.txt

pip install -r requirements.txt
python install.py

/pull repo

/set perms
sudo chmod 744 /home/cowmain/project/BarnPi/src/Cattle/cattle_startup.sh
sudo cp /home/cowmain/project/BarnPi/src/Cattle/startup.sh /usr/local/bin/cattle_startup.sh
sudo chmod 664 /home/cowmain/project/BarnPi/src/Cattle/cattle_startup.service
sudo cp /home/cowmain/project/BarnPi/src/Cattle/cattle_startup.service /etc/systemd/system/cattle_startup.service
sudo systemctl daemon-reload
sudo systemctl enable disk-space-check.service

sudo apt install -y avahi-daemon