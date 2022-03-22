class Stage:
    def __init__(self, data: dict):
        self.state = data.get('state', True)
        self.brightness = data.get('brightness', None)
        self.colour = data.get('colour', None)

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
