class Weapon:
    def __init__(self, props):
        self._id =  props['id_weapon']
        self._name = props['name']
        self._weapon_class = props['class']
        self._level = props['level']
        self._attack = props['attack']
        self._critical_hit = props['critical_hit']
        
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name

    @property
    def weapon_class(self):
        return self._weapon_class

    @property
    def weapon_level(self):
        return self._level

    @property
    def attack(self):
        return self._attack

    @property
    def critical_hit(self):
        return self._critical_hit
        
    def show_weapon_stats(self):
        print("----------------------------------------\n"
             f"{self._name} stats\n"
              "----------------------------------------\n"
             f"Class: {self._weapon_class}\n"
             f"Level: {self._level}\n"
             f"Attack: {self._attack}\n"
             f"Critical hit: {self._critical_hit}\n"
              "----------------------------------------")