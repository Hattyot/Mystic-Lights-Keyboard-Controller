# Mystic Lights keyboard controller
___
Very simple controller for mystic lights keyboard. \
Can be controller either through dbus commands or through configured keyboard shortcuts. \
Currently only static lights are available.

Special thanks to u/VesperLlama for providing the original script for this and 60-Keyboard.rules

## Vendor ID & Product ID
Vendor ID should always be 1462 \
Product ID varies and can be found out with `lsusb` command

## Installing
___
Before running `./install` configure config.yaml \
**Git:**
```
git clone https:://github.com/Hattyot/Mystic-Lights-Keyboard-Controller.git
cd Mystic-Lights-Keyboard-Controller
chmod +x install.sh start.sh
./install.sh
pip3 install -r requirements.txt
./start.sh
```
## Running
___
You can run the controller either through `./start.sh` or by running `mystic-lights-controller`