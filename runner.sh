#!/bin/bash
# to be run by crontab
set -e

python3 Main.py
sleep 60 * 5 # 5 minutes
