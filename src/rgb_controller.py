#!/usr/bin/env python
import usb.core
import usb.util
from config import Config
from profile import Profile


class DeviceNotFound(Exception):
    pass


class FailedToDetachKernelDriver(Exception):
    pass


class Controller:

    def __init__(self, config: Config):
        self.device = None

        self.current_profile = 0

        self.config = config
        self.profiles: list[Profile] = []

        self.load_device()
        self.load_profiles()

        # current state
        self.state = True  # default on
        self.brightness = 2  # default intensity of 2/5
        self.colour = [0xff, 0xff, 0xff]  # default colour of white

    def load_profiles(self):
        for i, profile_data in enumerate(self.config.profiles):
            profile = Profile(profile_data)
            self.profiles.append(profile)
            if profile.default:
                self.current_profile = i

        self.next_profile()

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
        old_profile = self.profiles[self.current_profile - 1]
        old_profile.current_stage = 0

        self.current_profile = (self.current_profile + 1) % len(self.profiles)
        self.next_stage()

    def next_stage(self):
        profile = self.profiles[self.current_profile - 1]
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
