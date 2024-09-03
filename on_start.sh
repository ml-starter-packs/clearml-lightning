#!/bin/bash

cd clearml-lightning && ./setup.sh && ./repair.sh && make up && \
cd agent && make up && \
echo "Done starting..."
