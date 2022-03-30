import asyncio
import sys
from config import Config
from rgb_controller import Controller
from keybind import KeyBinder
from gi.repository import GLib
from dbus.mainloop.glib import DBusGMainLoop
from dbusiface import DbusManager
from threading import Thread


def run_keybinder(config: Config, controller: Controller):
    if not config.hotkeys_enabled:
        return

    keybinds = {}
    if config.next_stage_hotkey:
        keybinds.update({config.next_stage_hotkey: controller.next_stage})
    if config.next_profile_hotkey:
        keybinds.update({config.next_profile_hotkey: controller.next_profile})

    KeyBinder.activate(keybinds)


def run_dbus(config: Config, controller: Controller):
    if not config.dbus_enabled:
        return

    DBusGMainLoop(set_as_default=True)
    DbusManager(config, controller)
    loop = GLib.MainLoop()
    loop.run()


async def run_interfaces(config: Config, controller: Controller):
    thread = Thread(target=run_keybinder, args=(config, controller))
    thread2 = Thread(target=run_dbus, args=(config, controller))

    thread.start()
    thread2.start()


def main():
    loop = asyncio.new_event_loop()
    config = Config()
    rgb_controller = Controller(config)

    loop.run_until_complete(run_interfaces(config, rgb_controller))


if __name__ == '__main__':
    main()
