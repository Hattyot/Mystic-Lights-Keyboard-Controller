#!/usr/bin/env python
import time

import usb.core
import usb.util
from config import Config


class DeviceNotFound(Exception):
    pass


class FailedToDetachKernelDriver(Exception):
    pass


class Controller:

    def __init__(self):
        self.device = None

        self.current_profile = 0

        self.config = Config()
        self.load_device()

        # current state
        self.state = True  # default on
        self.brightness = 2  # default intensity of 2/5
        self.colour = [0xff, 0xff, 0xff]  # default colour of white

    def load_device(self):
        light_device = usb.core.find(idVendor=self.config.vendor_id, idProduct=self.config.product_id)

        if light_device is None:
            raise DeviceNotFound()

        if light_device.is_kernel_driver_active(0) is True:
            try:
                light_device.detach_kernel_driver(0)
            except usb.core.USBError as e:
                raise FailedToDetachKernelDriver(e)

        self.device = light_device

    def next_profile(self):
        self.current_profile = (self.current_profile + 1) % len(self.config.profiles)
        self.next_stage()

    def next_stage(self):
        print('gi')
        profile = self.config.profiles[self.current_profile - 1]
        stage = profile.get_next_stage()
        self.state = stage.state

        if stage.colour:
            self.colour = stage.colour
        if stage.brightness:
            self.brightness = stage.brightness

        self.write_to_device()

    def write_to_device(self):
        # Store the packet data to send
        data = [0x02, 0x0] + [self.state] + [0x0] + [self.brightness] + [0x01] + self.colour + \
               [0xff, 0x50, 0x0, 0xff, 0xff, 0x0, 0x0, 0x10, 0xff, 0x0, 0x0, 0x0, 0xff,
                0x96, 0x0, 0xff, 0xff, 0x0, 0xff, 0x0, 0x0, 0x0, 0x0, 0x0, 0x20, 0x0, 0x0]

        self.device.ctrl_transfer(0x21, 0x9, 0x302, 0x0, data)

        usb.util.release_interface(self.device, 0)
#
# import usb.core
# import usb.util
# import os, sys
#
# # Help
# if str(sys.argv[1]) == "-h" or str(sys.argv[1]) == "--help":
#     print("""usage: changeRGB.py [colour] [brightness]
#
#         Colour         -       Enter Red, Green, Blue or White
#         Brightness     -       Enter number from 1-5 (Increasing intensity)""")
#     exit()
#
# VENDOR_ID = 0x1462
# PRODUCT_ID = 0x1563
#
# # Setup the USB ready for reads/writes
# global dev, interface
#
# dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
# interface = 0
#
# if dev is None:
# 	raise ValueError("Device is not connected")
#
# if dev.is_kernel_driver_active(interface) is True:
# 	try:
# 		dev.detach_kernel_driver(interface)
# 	except usb.core.USBError as e:
# 		raise ValueError("Failed to detach kernel driver: %s" % str(e))
#
# usb.util.claim_interface(dev,interface)
# dev.set_interface_altsetting(interface=interface, alternate_setting=0)
#
# state           =       [0x01]                  # Default State  - On
# brightness      =       [0x06]                  # Default Brightness - 3/5
# colour          =       [0xff, 0xff, 0xff]      # Default Colour - White
#
# # Set Colour
# if   sys.argv[1]    ==      "off"   :    state   =   [0x00]
# elif sys.argv[1]    ==      "red"   :    colour  =   [0xff, 0x00, 0x00]
# elif sys.argv[1]    ==      "green" :    colour  =   [0x00, 0xff, 0x00]
# elif sys.argv[1]    ==      "blue"  :    colour  =   [0x00, 0x00, 0xff]
#
# # Set Brightness if second argument is given else set default
# try:
#     if   sys.argv[2]    ==      "1"     :    brightness     =     [0x02]
#     elif sys.argv[2]    ==      "2"     :    brightness     =     [0x04]
#     elif sys.argv[2]    ==      "3"     :    brightness     =     [0x06]
#     elif sys.argv[2]    ==      "4"     :    brightness     =     [0x08]
#     elif sys.argv[2]    ==      "5"     :    brightness     =     [0x0a]
# except: pass
#
# # Store the packet data to send
# data = [0x02, 0x00] + state + [0x00] + brightness + [0x01] + colour + [ 0xff, 0x50, 0x00, 0xff, 0xff, 0x00, 0x00, 0x0010, 0xff, 0x00, 0x00, 0x00, 0xff, 0x96, 0x00, 0xff, 0xff, 0x00, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x0020, 0x00, 0x00]
#
#
# # Write to the usb device
# dev.ctrl_transfer(0x21, 0x09, 0x0302, 0x0000, data)
#
#
# # Reattach the kernel driver
# usb.util.release_interface(dev,interface)
# dev.attach_kernel_driver(interface)
