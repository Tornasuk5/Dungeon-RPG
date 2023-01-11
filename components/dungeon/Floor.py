class Floor:
    def __init__(self, floor_name, floor_description, level = 1):
        self._level = level
        self._name = floor_name
        self._description = floor_description

    @property
    def level(self):
        return self._level

    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description

                
