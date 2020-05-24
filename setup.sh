#!/bin/bash

git submodule update --init --recursive
apt-get install -y python3 python3-pip python3-dev
apt-get update
apt-get install software-properties-common -y
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update
apt-get install python3.7 -y
python3.7 -m pip install -r ./requirements.txt
python3.7 -u main_setup.py