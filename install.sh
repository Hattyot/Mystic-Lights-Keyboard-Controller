if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


cp 60-Keyboard.rules /etc/udev/rules.d/
cp org.hattyot.MysticLightRGB.conf /usr/share/dbus-1/system.d/

udevadm control -R
udevadm trigger

python -m pip install -r requirements.txt
ln -s $(realpath start.sh) /usr/local/bin/mystic-lights-controller