#!/bin/bash

cd clearml-lightning && make down && \
cd agent && make down && \
echo "Done stopping..."
