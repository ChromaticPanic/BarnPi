#!/bin/bash
time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/tx_data_to_nas.yaml | tee /home/rancher/Project/BarnPi/log/tx_data_to_nas.txt