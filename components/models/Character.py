import time
import math
import random

from components.models.Entity import Entity

class Character(Entity):

    def __init__(self, data, abilities):
        
        level = data['level'] if 'level' in data else 1
        
        super().__init__(data['hp'], data['mp'], data['stamina'], level, data['strength'], 
                        data['agility'], data['intellect'], data['attack'], data['defense'], 
                        data['critical_hit'], data['dodge'])

        self._name = data['name'] if 'name' in data else ""
        self._character_class = data['ref_class']
        self._luck = data['luck'] if 'luck' in data else random.randint(1, 10)
        self._floor_level = data['ref_floor_level'] if 'ref_floor_level' in data else 1
        self._abilities = abilities
        self._ability_power = 1.2 if self._character_class == "Mage" else 1.1
        self._ability_save = 0.2 if self._character_class == "Mage" else 0.1
        
    @property
    def name(self):
        return self._name

    @property
    def character_class(self):
        return self._character_class

    @property
    def luck(self):
        return self._luck

    @property
    def abilities(self):
        return self._abilities
        
    @property
    def floor_level(self):
        return self._floor_level
    
    @property
    def ability_power(self):
        return self._ability_power
    
    @ability_power.setter
    def ability_power(self, ability_power):
        self._ability_power = ability_power
        
    @property
    def ability_save(self):
        return self._ability_save
    
    @ability_save.setter
    def ability_save(self, ability_save):
        self._ability_save = ability_save
    
    @name.setter
    def name(self, name):
        self._name = name
    
    @luck.setter
    def luck(self, luck):
        self._luck = luck
        
    @abilities.setter
    def abilities(self, abilities):
        self._abilities = abilities
    
    @floor_level.setter
    def floor_level(self, floor_level):
        self._floor_level = floor_level
        
    #-------------------------
    # Gets character's full HP
    #-------------------------
    def get_full_hp(self):
        if self._character_class == "Hunter": full_hp = math.ceil(50 * self.level * 0.75)
        elif self._character_class == "Mage": full_hp = math.ceil(50 * self.level * 0.5)
        elif self._character_class == "Rogue": full_hp = math.ceil(50 * self.level * 0.7)
        elif self._character_class == "Warrior": full_hp = math.ceil(50 * self.level * 0.85)

        return full_hp
    
    #-------------------------
    # Gets character's full MP
    #-------------------------
    def get_full_mp(self):
        return math.ceil(30 * self.level * 0.7)
    
    #------------------------------
    # Gets character's full stamina
    #------------------------------
    def get_full_stamina(self):
        if self._character_class == "Hunter" or self._character_class == "Rogue":
            full_stamina = math.ceil(30 * self.level * 0.55)
        elif self._character_class == "Warrior": 
            full_stamina = math.ceil(30 * self.level * 0.75)

        return full_stamina
    
    #------------------
    # Character attacks
    #------------------
    def character_attack(self, monster):
        if self.stat_probability(monster.dodge):
            print(f"\n{monster.monster_type} DODGE your attack!")
        
        else:
            damage = self.attack - monster.defense
            
            if damage > 0:
            
                if self.stat_probability(self.critical_hit):
                    damage += round(damage * 0.5)
                    print("\nCRITICAL DAMAGE!")
                    time.sleep(1)
                    
                monster.hp -= damage
            
            else: damage = 0
            
            print(f"\n{self._name} deals {damage} damage to {monster.monster_type}")
            
        time.sleep(1)
            
    #--------------------------
    # Character uses an ability
    #--------------------------
    def character_ability(self, ability, monster):
        ability_cost = ability.resources_cost - math.floor((ability.resources_cost * self._ability_save))
        
        if self._character_class == "Hunter": self.stamina -= ability_cost
        elif self._character_class == "Mage": self.mp -= ability_cost
        elif self._character_class == "Rogue": self.stamina -= ability_cost
        elif self._character_class == "Warrior": self.stamina -= ability_cost
        
        if self.stat_probability(monster.dodge): 
            print(f"\n{monster.monster_type} DODGE your attack!")
        else:
            damage = math.ceil((ability.attack_power * self._ability_power)) - monster.defense
            
            if damage > 0:

                if self.stat_probability(self.critical_hit):
                    damage += round(damage * 0.5)
                    print("\nCRITICAL DAMAGE!")
                    time.sleep(1)
                
                monster.hp -= damage
                
            else: damage = 0

            print(f"\n{self._name} use '{ability.name}' and deals {damage} damage to {monster.monster_type}")
            
        time.sleep(1)
            
    #-------------------------------------------
    # Character consumes a potion from inventory
    #-------------------------------------------
    def consume_potion(self, potion):
        amount_rest = potion.amount_rest
        
        if potion.stat_rest == "HP":
            rest_hp = self.hp + amount_rest
            full_hp = self.get_full_hp()
            
            if rest_hp > full_hp:
                amount_rest = full_hp - self.hp
                rest_hp = full_hp
                
            self.hp = rest_hp
            
        elif potion.stat_rest == "MP":
            rest_mp = self.mp + amount_rest
            full_mp = self.get_full_mp()
            
            if rest_mp > full_mp:
                amount_rest = full_mp - self.mp
                rest_mp = full_mp
                
            self.mp = rest_mp
            
        elif potion.stat_rest == "Stamina":
            rest_stamina = self.stamina + amount_rest
            full_stamina = self.get_full_stamina()
            
            if rest_stamina > full_stamina:
                amount_rest = full_stamina - self.stamina
                rest_stamina = full_stamina
                
            self.stamina = rest_stamina
                
        print(f"You drink '{potion.name}' and restores +{amount_rest} {potion.stat_rest}")
        
    #------------------------
    # Shows character's stats
    #------------------------
    def show_character_stats(self):
        print("\n----------------------------------------\n"
             f"Name: {self._name}\n"
             f"Class: {self._character_class}\n"
             f"Level: {self.level}\n"
              "----------------------------------------\n"
             f"Stats\n"
             f"----------------------------------------\n"
             f"HP = {self.hp}               | Health Points -> Character's life\n" 
             f"MP = {self.mp}                | Mana Points -> Abilities' resource\n"
             f"Stamina = {self.stamina}          | Abilities' resource\n"
             f"Strength = {self.strength}          | + Attack / + Defense\n"
             f"Agility = {self.agility}           | + Critical damage / + Dodge\n"
             f"Intellect = {self.intellect}         | + Abilities damage / - Abilities cost\n"
             f"Attack = {self.attack}            | + Damage inflicted (attack and abilities)\n"
             f"Defense = {self.defense}           | - Damage from monsters\n"
             f"Critical hit = {self.critical_hit}   | + Probability of causing critical damage\n"
             f"Dodge = {self.dodge}          | + Probability of dodging a monster's attack\n"
             f"Luck = {self._luck}              | + Probability of encountering loot chests and finding rest places\n"
              "----------------------------------------")
            
    #--------------------------------------------------
    # Level UP -> Increases the character's basic stats
    #--------------------------------------------------
    def level_up(self):
        self.level += 1
        
        if self._character_class == "Hunter":
            self.hp = math.ceil(50 * self.level * 0.75)
            self.stamina = math.ceil(30 * self.level * 0.55)

        elif self._character_class == "Mage": 
            self.hp = math.ceil(50 * self.level * 0.5)
            self.mp = math.ceil(30 * self.level * 0.7)

        elif self._character_class == "Rogue": 
            self.hp = math.ceil(50 * self.level * 0.7)
            self.stamina = math.ceil(30 * self.level * 0.55)

        elif self._character_class == "Warrior": 
            self.hp = math.ceil(50 * self.level * 0.85)
            self.stamina = math.ceil(30 * self.level * 0.75)
            
        
    #-----------------------------------------------------------------------------------
    # Level UP -> Increases one of the three main stats (strength, agility or intellect)
    #-----------------------------------------------------------------------------------
    def stats_up(self, stat):
        if stat == "Strength":
            self.strength += 1
            if self._character_class == "Hunter": 
                self.attack = math.ceil(self.attack + (self.strength * 0.2))
                self.defense =  math.ceil(self.defense + (self.strength * 0.2))

            elif self._character_class == "Mage": 
                self.attack = math.ceil(self.attack + (self.strength * 0.1))
                self.defense =  math.ceil(self.defense + (self.strength * 0.1))

            elif self._character_class == "Rogue": 
                self.attack = math.ceil(self.attack + (self.strength * 0.25))
                self.defense =  math.ceil(self.defense + (self.strength * 0.15))

            elif self._character_class == "Warrior": 
                self.attack = math.ceil(self.attack + (self.strength * 0.3))
                self.defense =  math.ceil(self.defense + (self.strength * 0.3))
            
        elif stat == "Agility":
            self.agility += 1
            if self._character_class == "Hunter": 
                self.critical_hit = math.ceil(self.agility * 1 * 5)
                self.dodge =  math.ceil(self.agility * 0.5 * 5)

            elif self._character_class == "Mage": 
                self.critical_hit = math.ceil(self.agility * 0.5 * 5)
                self.dodge =  math.ceil(self.agility * 0.3 * 5)

            elif self._character_class == "Rogue": 
                self.critical_hit = math.ceil(self.agility * 2 * 5)
                self.dodge =  math.ceil(self.agility * 1 * 5)

            elif self._character_class == "Warrior": 
                self.critical_hit = math.ceil(self.agility * 0.75 * 5)
                self.dodge =  math.ceil(self.agility * 0.25 * 5)
                
        elif stat == "Intellect":
            self.intellect += 1
            if self._character_class == "Hunter" or self._character_class == "Rogue":
                self._ability_power = self.ability_power + 0.05
                self._ability_save = self._ability_save + 0.05

            elif self._character_class == "Mage":
                self._ability_power = self.ability_power + 0.075
                self._ability_save = self._ability_save + 0.075

            elif self._character_class == "Warrior":
                self._ability_power = self.ability_power + 0.03
                self._ability_save = self._ability_save + 0.03

    #----------------------------------------------
    # Gets character's class main resource (string)
    #----------------------------------------------
    def get_class_main_resource(self):
        if self._character_class == "Hunter" or self._character_class == "Rogue" or self._character_class == "Warrior":
            class_main_res = "Stamina"
        elif self._character_class == "Mage": 
            class_main_res = "MP"
        
        return class_main_res
    
    #-------------------------------------------------------------
    # Recharges a bit the character's main resource after an event
    #-------------------------------------------------------------
    def auto_recharge_res(self):
        if self._character_class == "Hunter" or self._character_class == "Rogue" or self._character_class == "Warrior":
            if self.stamina < self.get_full_stamina():
                self.stamina += 1
        elif self._character_class == "Mage":
            if self.mp < self.get_full_mp():
                self.mp += 1