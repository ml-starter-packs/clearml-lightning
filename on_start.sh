#!/bin/bash

cd clearml-lightning && ./setup.sh && ./repair.sh && make up && cd ..
cd agent && make up
