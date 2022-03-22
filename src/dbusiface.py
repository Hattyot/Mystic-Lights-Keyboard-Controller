import rgb_controller
import dbus
import dbus.service
from keybind import KeyBinder
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop

DBUS_PATH = "/org/hattyot/MysticLightRGB"
DBUS_NAME = "org.hattyot.MysticLightRGB"


class DbusManager(dbus.service.Object):
    def __init__(self):
        self.rgb_controller = rgb_controller.Controller()
        self.config = self.rgb_controller.config

        self.bus = dbus.SystemBus()
        bus_name = dbus.service.BusName(DBUS_NAME, bus=self.bus)

        self.setup_keybinds()
        super(DbusManager, self).__init__(bus_name, DBUS_PATH)

    def setup_keybinds(self):
        keybinds = {}
        if self.config.next_stage_hotkey:
            keybinds.update({self.config.next_stage_hotkey: self.next_stage})
        if self.config.next_profile_hotkey:
            keybinds.update({self.config.next_profile_hotkey: self.next_profile})

        KeyBinder.activate(keybinds)

    @dbus.service.method(DBUS_NAME)
    def next_stage(self, *_, **__):
        self.rgb_controller.next_stage()

    @dbus.service.method(DBUS_NAME)
    def next_profile(self, *_, **__):
        self.rgb_controller.next_profile()


def run_dbus_service():
    DBusGMainLoop(set_as_default=True)
    DbusManager()
    loop = GLib.MainLoop()
    loop.run()


if __name__ == '__main__':
    run_dbus_service()
