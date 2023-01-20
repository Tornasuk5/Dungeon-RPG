class MonsterAbility:
    def __init__(self, props):
        self._id = props['id_ability']
        self._name = props['name']
        self._attack_power = props['attack_power']
        self._res_cost = props['resources_cost']
        self._prob = props['probability']

    @property
    def level(self):
        return self._level

    @property
    def name(self):
        return self._name

    @property
    def attack_power(self):
        return self._attack_power

    @property
    def resources_cost(self):
        return self._res_cost
    
    @property
    def probability(self):
        return self._prob