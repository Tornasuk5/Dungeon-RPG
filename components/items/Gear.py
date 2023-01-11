class Gear:
    def __init__(self, props):
        self._id =  props['id_gear']
        self._name = props['name']
        self._gear_class = props['class']
        self._level = props['level']
        self._defense = props['defense']
        self._dodge = props['dodge']
        
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name

    @property
    def gear_class(self):
        return self._gear_class

    @property
    def gear_level(self):
        return self._level

    @property
    def defense(self):
        return self._defense

    @property
    def dodge(self):
        return self._dodge

    def show_gear_stats(self):
        print("----------------------------------------\n"
             f"{self._name} stats\n"
              "----------------------------------------\n"
             f"Class: {self._gear_class}\n"
             f"Level: {self._level}\n"
             f"Defense: {self._defense}\n"
             f"Dodge: {self._dodge}\n"
              "----------------------------------------")