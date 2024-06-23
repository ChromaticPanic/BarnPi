#!/bin/bash
time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/capture_frames.yaml | tee capture_frames.txt