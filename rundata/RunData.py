import copy
import random
from components.dungeon.Floor import Floor
from components.models.Character import Character
from database.DBManager import DBManager

class RunData:
    def __init__(self):
        self.PROB_BATTLE = 30 # Enemy encounter
        self.PROB_TRAP = 25 # Trap chest probability
        self.PROB_MONSTER_ABILITY = 25 # Use of an enemy's ability probability
        
        self._db_manager = DBManager()
        
        self._character = Character(dict.fromkeys(("hp", "mp", "stamina", "strength", "agility", 
                                                  "intellect", "attack", "defense", "critical_hit", "dodge", "name", 
                                                  "ref_class", "luck", "ref_floor_level")), [])
        self._prob_list = []
        
        self.__level = 1

        self._floor = Floor(self._db_manager.rpgdao.get_floor_name(self.__level), 
                            self._db_manager.rpgdao.get_floor_description(self.__level))
        
        self._floor_monsters = []
        
    @property
    def db_manager(self):
        return self._db_manager
    
    @property
    def floor(self):
        return self._floor
    
    @property
    def prob_list(self):
        return self._prob_list
    
    @property
    def floor_monsters(self):
        return self._floor_monsters
    
    @property
    def character(self):
        return self._character
    
    @character.setter
    def character(self, character):
        self._character = character
        
    # --------------------------
    # Sets events' probabilities
    # --------------------------
    def set_probabilities(self):
        prob_loot = int(20 + self._character.luck) # Loot encounter probability
        prob_rest_place = int(20 + self._character.luck) # Rest place encounter probability
        prob_carry_on = int(100 - (self.PROB_BATTLE + prob_loot + prob_rest_place)) # No event probability
        
        for i in range(1, self.PROB_BATTLE): self._prob_list.append("battle")
        for i in range(1, prob_loot): self._prob_list.append("loot")
        for i in range(1, prob_rest_place): self._prob_list.append("rest")
        for i in range(1, prob_carry_on): self._prob_list.append("")
    
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
        self._floor = Floor(self._db_manager.rpgdao.get_floor_name(self.__level), 
                            self._db_manager.rpgdao.get_floor_description(self.__level), self.__level)
        
    # -----------------------------------------------------------
    # Gets random monsters with the same level as the floor level
    # -----------------------------------------------------------
    def set_random_monsters(self):
        monsters = self._db_manager.rpgdao.get_level_monsters(self.__level)

        for i in range(0, 5): 
            monster = copy.deepcopy(random.choice(monsters))
            self._floor_monsters.append(monster)

        
