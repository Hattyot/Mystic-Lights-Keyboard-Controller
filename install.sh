if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi


cp 60-Keyboard.rules /etc/udev/rules.d/60-Keyboard.rules
udevadm control -R
udevadm trigger
python -m pip install -r requirements.txt
ln -s $(realpath start.sh) /usr/local/bin/mystic-lights-controller