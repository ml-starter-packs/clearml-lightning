#!/bin/sh

echo "Attempting to repair mongo"
docker run --rm -v ~/opt/clearml/data/mongo_4/db:/data/db mongo:4.4.28 mongod --dbpath /data/db --repair
