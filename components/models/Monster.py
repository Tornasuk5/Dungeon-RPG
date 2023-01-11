import time
import random

from components.models.Entity import Entity

class Monster(Entity):

    def __init__(self, data, abilities):
        super().__init__(data['hp'], data['mp'], data['stamina'], data['level'], 
                         data['strength'], data['agility'], data['intellect'], 
                         data['attack'], data['defense'], data['critical_hit'], data['dodge'])
        
        self._monster_type = data['monster_type']
            
        self._abilities = abilities

    @property
    def monster_type(self):
        return self._monster_type

    @property
    def abilities(self):
        return self._abilities

    def monster_attack(self, character):
        dodge_random = random.randint(0, 100)
        
        if dodge_random <= character.dodge: print("You DODGE enemy's attack!")
        
        else:
            damage = self.attack - character.defense
            
            if damage > 0:
                critical_hit_random = random.randint(0, 100)
                
                if critical_hit_random <= self.critical_hit:
                    damage += round(damage * 0.5)
                    print("CRITICAL DAMAGE!")
                    
                character.hp = character.hp - damage
                
            else: damage = 0

            print(f"{self._monster_type} deals {str(damage)} damage to {character.name}")
            
            
    def monster_ability(self, ability, character):
        self.cast_ability(ability.resources_cost)
        
        dodge_random = random.randint(0, 100)
        
        if dodge_random <= character.dodge: print("You DODGE enemy's attack!")
        
        else:
            damage = ability.attack_power - character.defense
            
            if damage > 0:
                critical_hit_random = random.randint(0, 100)
                
                if critical_hit_random <= self.critical_hit:
                    damage += round(damage * 0.5)
                    print("CRITICAL DAMAGE!")
                    
                character.hp = character.hp - damage

            print(f"{self._monster_type} use '{ability.name}' and deals {damage} damage to {character.name}")
            
        
    def show_monster_stats(self):
        print("----------------------------------------\n"
             f"Monster: {self._monster_type}\n"
             f"Level: {self.level}\n"
             f"Floor level: {self.floor_level}\n"
              "----------------------------------------\n"
             f"data\n"
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
              "----------------------------------------") 
        
    def get_main_resource(self):
        if self._monster_type == "Undead": main_res = self.stamina
        elif self._monster_type == "Goblin": main_res = self.stamina
        elif self._monster_type == "Cave Spider": main_res = self.stamina
        elif self._monster_type == "Skeleton Warrior": main_res = self.stamina
        elif self._monster_type == "Dungeon Lizard": main_res = self.stamina
        elif self._monster_type == "Imp": main_res = self.mp
        elif self._monster_type == "Hellhound": main_res = self.stamina
        elif self._monster_type == "Shadow": main_res = self.mp
        elif self._monster_type == "Minotaur": main_res = self.stamina
        elif self._monster_type == "Stone Guardian": main_res = self.stamina
        elif self._monster_type == "Crystal Scorpion": main_res = self.stamina
        elif self._monster_type == "Wyvern": main_res = self.stamina
        elif self._monster_type == "Silver Fang": main_res = self.stamina
        elif self._monster_type == "Behemoth": main_res = self.mp
        elif self._monster_type == "Daemon": main_res = self.mp
        elif self._monster_type == "Reaper": main_res = self.mp
        elif self._monster_type == "Elder Lich": main_res = self.mp
        elif self._monster_type == "Obsidian Guardian": main_res = self.stamina
        elif self._monster_type == "Arachne": main_res = self.mp
        elif self._monster_type == "Black Dragon": main_res = self.mp
        
        return main_res
    
    def cast_ability(self, cost):
        if self._monster_type == "Undead": self.stamina -= cost
        elif self._monster_type == "Goblin": self.stamina -= cost
        elif self._monster_type == "Cave Spider": self.stamina -= cost
        elif self._monster_type == "Skeleton Warrior": self.stamina -= cost
        elif self._monster_type == "Dungeon Lizard": self.stamina -= cost
        elif self._monster_type == "Imp": self.mp -= cost
        elif self._monster_type == "Hellhound": self.stamina -= cost
        elif self._monster_type == "Shadow": self.mp -= cost
        elif self._monster_type == "Minotaur": self.stamina -= cost
        elif self._monster_type == "Stone Guardian": self.stamina -= cost
        elif self._monster_type == "Crystal Scorpion": self.stamina -= cost
        elif self._monster_type == "Wyvern": self.stamina -= cost
        elif self._monster_type == "Silver Fang": self.stamina -= cost
        elif self._monster_type == "Behemoth": self.mp -= cost
        elif self._monster_type == "Daemon": self.mp -= cost
        elif self._monster_type == "Reaper": self.mp -= cost
        elif self._monster_type == "Elder Lich": self.mp -= cost
        elif self._monster_type == "Obsidian Guardian": self.stamina -= cost
        elif self._monster_type == "Arachne": self.mp -= cost
        elif self._monster_type == "Black Dragon": self.mp -= cost

            
