# Mystic Lights keyboard controller
___
Very simple controller for mystic lights keyboard. \
Can be controller either through dbus commands or through configured keyboard shortcuts. \
Currently only static lights are available.

Special thanks to u/VesperLlama for providing the original script for this and 60-Keyboard.rules

## Config
All configurable things can be configured in `config.yaml`
* `vendor_id` - Should always be 1462
* `product_id` - Varies on devices and can be found out with `lsusb` command
* `dbus_enabled` - Whether to enable dbus
* `hotkeys_enabled` - Whether to enable all hotkeys or not
* `next_stage_hotkey` - if set, automatically creates a global hotkey for switching stages
* `next_profile_hotkey` - if set, automatically creates a global hotkey for switching profiles
## Profiles
Profiles can be configured in `config.yaml`
* `name` - name assigned to the profile
* `default` - if yes, will always default to that profile on launch
* `stages`
  * `state` - turn the lights on or off
  * `brightness` - value between 1-5, sets the brightness of the lights
  * `colour` - array of red, green and blue values between 1-255. \
    Also accepts hex colour and colour names (results may vary)

Stage notes:
* if a value like `colour` or `brightness` is skipped on a stage, it inherits the values from the previous stage
## Installing
___
Before running `./install` configure config.yaml \
When using the service, you might need to install requirements under root.\
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