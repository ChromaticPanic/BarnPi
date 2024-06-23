#!/bin/bash
time ansible-playbook -i /home/rancher/Project/BarnPi/src/Rancher/hosts.ini /home/rancher/Project/BarnPi/src/Rancher/sync_to_public.yaml | tee sync_to_public.txt