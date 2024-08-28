#!/bin/bash

echo "vm.max_map_count=262144" > /tmp/99-clearml.conf
sudo mv /tmp/99-clearml.conf /etc/sysctl.d/99-clearml.conf
sudo sysctl -w vm.max_map_count=262144
sudo service docker restart

mkdir -p ~/opt/clearml/data/elastic_7
mkdir -p ~/opt/clearml/data/mongo_4/db
mkdir -p ~/opt/clearml/data/mongo_4/configdb
mkdir -p ~/opt/clearml/data/redis
mkdir -p ~/opt/clearml/logs
mkdir -p ~/opt/clearml/config
mkdir -p ~/opt/clearml/data/fileserver

# mkdir -p ~/usr/share/elasticsearch/logs
