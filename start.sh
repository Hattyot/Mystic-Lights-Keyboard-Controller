#!/bin/bash
cd "$(dirname "$(realpath "$0")")"
export $(dbus-launch)
export DISPLAY=:0
python src/dbusiface.py
