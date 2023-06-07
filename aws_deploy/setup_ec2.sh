#!/bin/bash

#install main libraries
sudo yum install docker

# add user to docker group
sudo usermod -a -G docker ec2-user

# install docker-compose
wget https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) 
sudo mv docker-compose-$(uname -s)-$(uname -m) /usr/local/bin/docker-compose
sudo chmod -v +x /usr/local/bin/docker-compose

sudo reboot