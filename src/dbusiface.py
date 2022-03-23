import dbus
import dbus.service
from rgb_controller import Controller
from config import Config


DBUS_PATH = "/org/hattyot/MysticLightRGB"
DBUS_NAME = "org.hattyot.MysticLightRGB"


class DbusManager(dbus.service.Object):
    def __init__(self, config: Config, controller: Controller):
        self.config = config
        self.rgb_controller = controller

        self.bus = dbus.SystemBus()
        bus_name = dbus.service.BusName(DBUS_NAME, bus=self.bus)

        super(DbusManager, self).__init__(bus_name, DBUS_PATH)

    @dbus.service.method(DBUS_NAME)
    def next_stage(self, *_, **__):
        self.rgb_controller.next_stage()

    @dbus.service.method(DBUS_NAME)
    def next_profile(self, *_, **__):
        self.rgb_controller.next_profile()
