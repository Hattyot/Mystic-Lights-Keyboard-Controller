import re
import webcolors


class Stage:
    def __init__(self, data: dict):
        self.state = data.get('state', True)
        self.brightness = data.get('brightness')
        self.colour = self.parse_colour(data.get('colour'))

    @staticmethod
    def parse_colour(colour_data):
        if isinstance(colour_data, list) and len(colour_data) == 3:
            return colour_data
        elif isinstance(colour_data, str) and re.match('^#(?:[0-9a-fA-F]{3}){1,2}$', colour_data):
            return [int(x, 16) for x in re.findall('..', re.findall('^(?:#)?((?:[0-9a-fA-F]{3}){1,2})$', '#ffffff')[0])]
        elif isinstance(colour_data, str):
            return list(webcolors.name_to_rgb(colour_data))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = [
            f"State: {'on' if self.state else 'off'}",
            f"Brightness: {self.brightness}" if self.brightness else '',
            f"Colour: #{''.join(hex(x)[2:] for x in self.colour)}" if self.colour else ''
        ]
        return "<" + ', '.join([s for s in string if s]) + ">"


class Profile:
    def __init__(self, data: dict):
        self.name = data.get('name', None)
        self.default = data.get('default', False)
        self.stages: list[Stage] = [Stage(stage_data) for stage_data in data['stages']]
        self.current_stage = 0

    def get_next_stage(self):
        self.current_stage = (self.current_stage + 1) % len(self.stages)
        return self.stages[self.current_stage - 1]

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        string = [
            f"Name: {self.name}" if self.name else '',
            f"Default: {self.default}" if self.default else '',
            f"Stages: {[stage for stage in self.stages]}" if self.stages else ''
        ]
        return "<" + ', '.join([s for s in string if s]) + ">"
