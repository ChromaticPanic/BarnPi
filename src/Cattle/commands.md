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