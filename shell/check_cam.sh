#!/bin/bash
time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/check_cam.yaml | tee /home/rancher/Project/BarnPi/log/check_cam.txt