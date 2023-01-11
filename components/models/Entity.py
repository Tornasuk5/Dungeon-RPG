class Entity():
    def __init__(self, hp, mp, stamina, level, strength, agility, intellect, attack, defense, critical_hit, dodge):
        self._level = level
        self._hp = hp
        self._mp = mp
        self._stamina = stamina
        self._strength = strength
        self._agility = agility
        self._intellect = intellect
        self._attack = attack
        self._defense = defense
        self._critical_hit = critical_hit
        self._dodge = dodge

    @property
    def level(self):
        return self._level
    
    @property    
    def hp(self):
        return self._hp

    @property
    def mp(self):
        return self._mp

    @property
    def stamina(self):
        return self._stamina
    
    @property
    def strength(self):
        return self._strength
    
    @property
    def agility(self):
        return self._agility
    
    @property
    def intellect(self):
        return self._intellect
    
    @property
    def attack(self):
        return self._attack

    @property
    def defense(self):
        return self._defense

    @property
    def critical_hit(self):
        return self._critical_hit

    @property
    def dodge(self):
        return self._dodge
    
    @level.setter
    def level(self, level):
        self._level = level
    
    @hp.setter
    def hp(self, hp):
        self._hp = hp

    @mp.setter
    def mp(self, mp):
        self._mp = mp
        
    @stamina.setter
    def stamina(self, stamina):
        self._stamina = stamina

    @strength.setter
    def strength(self, strength):
        self._strength = strength
    
    @agility.setter
    def agility(self, agility):
        self._agility = agility

    @intellect.setter
    def intellect(self, intellect):
        self._intellect = intellect

    @attack.setter
    def attack(self, attack):
        self._attack = attack
    
    @defense.setter
    def defense(self, defense):
        self._defense = defense

    @critical_hit.setter
    def critical_hit(self, critical_hit):
        self._critical_hit = critical_hit

    @dodge.setter
    def dodge(self, dodge):
        self._dodge = dodge