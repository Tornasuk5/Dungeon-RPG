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
        
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

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
    
    @luck.setter
    def luck(self, luck):
        self._luck = luck
    
    @floor_level.setter
    def floor_level(self, floor_level):
        self._floor_level = floor_level

    def get_full_hp(self):
        if self._character_class == "Archer": full_hp = math.ceil((50 + (50 * self.level * 0.5)))
        elif self._character_class == "Mage": full_hp = math.ceil((50 + (50 * self.level * 0.25)))
        elif self._character_class == "Rogue": full_hp = math.ceil((50 + (50 * self.level * 0.4)))
        elif self._character_class == "Warrior": full_hp = math.ceil((50 + (50 * self.level * 0.6)))

        return full_hp
    
    def get_full_mp(self):
        return math.ceil((25 + (25 * self.level * 0.75)))
    
    def get_full_stamina(self):
        if self._character_class == "Archer": full_stamina = math.ceil((25 + (25 * self.level * 0.5)))
        elif self._character_class == "Rogue": full_stamina = math.ceil((25 + (25 * self.level * 0.6)))
        elif self._character_class == "Warrior": full_stamina = math.ceil((25 + (25 * self.level * 0.4)))

        return full_stamina
    

    def character_attack(self, monster):
        dodge_random = random.randint(0, 100)
        
        if dodge_random <= monster.dodge: print(f"{monster.monster_type} DODGE your attack!")
        
        else:
            damage = self.attack - monster.defense
            
            if damage > 0:
                
                critical_hit_random = random.randint(0, 100)
                
                if critical_hit_random <= self.critical_hit:
                    damage += round(damage * 0.5)
                    print("CRITICAL DAMAGE!")
                    
                monster.hp = monster.hp - damage
            
            else: damage = 0
            
            print(f"{self._name} deals {damage} damage to {monster.monster_type}")
            time.sleep(1)
            
            
    def character_ability(self, ability, monster):
        self.cast_ability(ability.resources_cost)
        
        dodge_random = random.randint(0, 100)
        
        if dodge_random <= monster.dodge: print(f"{monster.monster_type} DODGE your attack!")
        
        else:
            damage = ability.attack_power - monster.defense
            
            if damage > 0:
                
                critical_hit_random = random.randint(0, 100)
                
                if critical_hit_random <= self.critical_hit:
                    damage += round(damage * 0.5)
                    print("CRITICAL DAMAGE!")
                
                monster.hp = monster.hp - damage
                
            else: damage = 0

            print(f"{self._name} use '{ability.name}' and deals {damage} damage to {monster.monster_type}")
            time.sleep(1)
            

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
        

    def show_character_stats(self):
        print("----------------------------------------\n"
             f"Name: {self._name}\n"
             f"Class: {self._character_class}\n"
             f"Level: {self.level}\n"
             f"Floor level: {self.floor_level}\n"
              "----------------------------------------\n"
             f"Stats\n"
             f"----------------------------------------\n"
             f"HP = {self.hp}\n" 
             f"MP = {self.mp}\n"
             f"Stamina = {self.stamina}\n"
             f"Strength = {self.strength}\n"
             f"Agility = {self.agility}\n"
             f"Intellect = {self.intellect}\n"
             f"Attack = {self.attack}\n"
             f"Defense = {self.defense}\n"
             f"Critical hit = {self.critical_hit}\n"
             f"Dodge = {self.dodge}\n"
             f"Luck = {self._luck}\n"
              "----------------------------------------")
        
        
    def level_up(self):
        self.level = self.level + 1
        self.strength = self.strength + 1
        self.agility = self.agility + 1
        self.intellect = self.intellect + 1
        
        if self._character_class == "Archer": 
            incr_percent_class = [0.5, 0.5]
            self.stamina = math.ceil((25 + (25 * self.level * incr_percent_class[1])))

        elif self._character_class == "Mage": 
            incr_percent_class = [0.25, 0.75]
            self.mp = math.ceil((25 + (25 * self.level * incr_percent_class[1])))

        elif self._character_class == "Rogue": 
            incr_percent_class = [0.4, 0.6]
            self.stamina = math.ceil((25 + (25 * self.level * incr_percent_class[1])))

        elif self._character_class == "Warrior": 
            incr_percent_class = [0.6, 0.4]
            self.stamina = math.ceil((25 + (25 * self.level * incr_percent_class[1])))
        
        self.hp = math.ceil((50 + (50 * self.level * incr_percent_class[0])))
    
        
    def get_main_resource(self):
        if self._character_class == "Archer": main_res = self.stamina
        elif self._character_class == "Mage": main_res = self.mp
        elif self._character_class == "Rogue": main_res = self.stamina
        elif self._character_class == "Warrior": main_res = self.stamina
        
        return main_res
    
    def cast_ability(self, cost):
        if self._character_class == "Archer": self.stamina -= cost
        elif self._character_class == "Mage": self.mp -= cost
        elif self._character_class == "Rogue": self.stamina -= cost
        elif self._character_class == "Warrior": self.stamina -= cost
        
        
    def set_new_abilities(self, new_abilities):
        self._abilities = new_abilities

    



    

    

