import copy
import random
from components.dungeon.floor import Floor
from components.models.character import Character
from sqlite.rpgdao import RpgDao

class RunData:
    def __init__(self):
        self.__PROB_BATTLE = 17 # Character fights a monster
        self.__PROB_TRAP = 25 # Trap chest probability
        self.__PROB_MONSTER_ABILITY = 20 # Use of an monster's ability probability
        
        self._rpgdao = RpgDao()
        
        self._character = Character(dict.fromkeys(("hp", "mp", "stamina", "strength", "agility", 
                                                  "intellect", "attack", "defense", "critical_hit", "dodge", "name", 
                                                  "ref_class", "luck", "ref_floor_level")), [])
        
        self.__level = 1

        self._floor = Floor(self._rpgdao.get_floor_name(self.__level), self._rpgdao.get_floor_description(self.__level))
        
        self._floor_monsters = []
        
    @property
    def rpgdao(self):
        return self._rpgdao
    
    @property
    def floor(self):
        return self._floor
    
    @property
    def floor_monsters(self):
        return self._floor_monsters
    
    @property
    def character(self):
        return self._character
    
    @character.setter
    def character(self, character):
        self._character = character
        
    # -------------------------
    # Get events' random choice
    # -------------------------
    def get_random_choice(self, event):
        choices = []
        probabilities = []
        
        if event == "main":
            prob_loot = int(5 + self._character.luck) # Loot encounter probability
            prob_rest_place = int(5 + self._character.luck) # Rest place encounter probability
            prob_carry_on = int(100 - (self.__PROB_BATTLE + prob_loot + prob_rest_place)) # No event probability
            
            choices = ["battle", "loot", "rest", "carry_on"]
            probabilities = [self.__PROB_BATTLE, prob_loot, prob_rest_place, prob_carry_on]
            
        elif event == "monster":
            choices = ["ability", "attack"]
            probabilities = [self.__PROB_MONSTER_ABILITY, 100 - self.__PROB_MONSTER_ABILITY]
            
        elif event == "loot":
            choices = ["trap", "chest"]
            trap_probability = self.__PROB_TRAP - self._character.luck
            probabilities = [trap_probability, 100 - trap_probability]
        
        return random.choices(choices, probabilities)[0]
    
    # ---------------------------------------------
    # Picks a monster from the floor_monsters array
    # ---------------------------------------------
    def get_monster(self):
        return self._floor_monsters.pop()
    
    # ----------------------
    # Sets a new floor level
    # ----------------------
    def new_floor_level(self):
        self.__level += 1
        self._floor = Floor(self._rpgdao.get_floor_name(self.__level), 
                            self._rpgdao.get_floor_description(self.__level), self.__level)
        
    # -----------------------------------------------------------
    # Gets random monsters with the same level as the floor level
    # -----------------------------------------------------------
    def set_random_monsters(self):
        monsters = self._rpgdao.get_level_monsters(self.__level)

        for i in range(5): 
            monster = copy.deepcopy(random.choice(monsters))
            self._floor_monsters.append(monster)
        
