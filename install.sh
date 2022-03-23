if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

set -x

vendor_id=$(grep -oP 'vendor_id:\s+\K(\d+)' config.yaml)
product_id=$(grep -oP 'product_id:\s+\K(\d+)' config.yaml)
keyboard_rules="SUBSYSTEMS==\"usb\", ATTR{idVendor}==\"${vendor_id}\", ATTR{idProduct}==\"${product_id}\", TAG+=\"uaccess\""

echo "${keyboard_rules}" > /etc/udev/rules.d/60-Keyboard.rules
cp org.hattyot.MysticLightRGB.conf /usr/share/dbus-1/system.d/

udevadm control -R
udevadm trigger

ln -s $(realpath start.sh) /usr/local/bin/mystic-lights-controller