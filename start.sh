#!/bin/bash
cd "$(dirname "$(realpath "$0")")"
export $(dbus-launch)
python src/dbusiface.py