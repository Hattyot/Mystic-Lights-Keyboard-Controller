import yaml
from profile import Profile


class Config:
    def __init__(self):
        self.vendor_id = None
        self.product_id = None

        self.dbus_enabled = None
        self.hotkeys_enabled = None
        self.next_stage_hotkey = None
        self.next_profile_hotkey = None

        self.profiles: list[dict] = []

        self.load_config()

    def load_config(self):
        with open('config.yaml', 'r') as config:
            config = yaml.safe_load(config)

        self.vendor_id = int(str(config['config']['vendor_id']), 16)
        self.product_id = int(str(config['config']['product_id']), 16)

        self.dbus_enabled = config['config'].get('dbus_enabled')
        self.hotkeys_enabled = config['config'].get('hotkeys_enabled')
        self.next_stage_hotkey = config['config'].get('next_stage_hotkey')
        self.next_profile_hotkey = config['config'].get('next_profile_hotkey')

        self.profiles = config['profiles']
