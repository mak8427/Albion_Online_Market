#!/bin/bash
# to be run by crontab
set -e

python3.11 Main.py
sleep 300 # 5 minutes
