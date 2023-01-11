class Potion:
    def __init__(self, props):
        self._id =  props['id_potion']
        self._name = props['name']
        self._level = props['level']
        self._stat_rest = props['stat_rest']
        self._amount_rest = props['amount_rest']
        
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name

    @property
    def potion_level(self):
        return self._level

    @property
    def stat_rest(self):
        return self._stat_rest

    @property
    def amount_rest(self):
        return self._amount_rest
    
    def show_potion_stats(self):
        print("----------------------------------------\n"
             f"{self._name} stats\n"
              "----------------------------------------\n"
             f"Level: {self._level}\n"
             f"Stat Restitution: {self._stat_rest}\n"
             f"Amount Restitution: {self._amount_rest}\n"
              "----------------------------------------")
