#!/bin/bash
time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/mount_nas.yaml | tee /home/rancher/Project/BarnPi/log/mount_nas.txt