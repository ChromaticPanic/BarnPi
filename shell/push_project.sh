#!/bin/bash
time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/push_project_to_hosts.yaml | tee push_project_to_hosts.txt