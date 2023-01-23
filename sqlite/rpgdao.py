import sqlite3

from components.items.potion import Potion
from components.items.gear import Gear
from components.items.weapon import Weapon
from components.models.character import Character
from components.models.monster import Monster
from components.abilities.character_ability import CharacterAbility
from components.abilities.monster_ability import MonsterAbility

class RpgDao:
    def __init__(self):
        self.__dungeon_db = sqlite3.connect("sqlite/database/dungeon_rpg.db")
        self._cursor = self.__dungeon_db.cursor()
        
    #-----------------------------------------------------
    # Saves (modifies) character's stats into the database
    #-----------------------------------------------------
    def auto_save_game(self, character: Character):
        update_query = "UPDATE characters SET level = ?, hp = ?, mp = ?, stamina = ?, strength = ?, agility = ?, intellect = ?, attack = ?, defense = ?, critical_hit = ?, dodge = ?, luck = ?, ref_floor_level = ? WHERE name = ?"
        
        values = (character.level, character.hp, character.mp, character.stamina, character.strength, 
                    character.agility, character.intellect, character.attack, character.defense,
                    character.critical_hit, character.dodge, character.luck, character.floor_level, character.name)

        self._cursor.execute(update_query, values)
        
        self.__dungeon_db.commit()
            
    #-------------------------------------------
    # Character consumes a potion from inventory
    #-------------------------------------------
    def use_potion(self, character_name, potion_id):
        self._cursor.execute("SELECT id_cp FROM characters_potions " +
                    "WHERE ref_character = ? AND ref_potion = ? " +
                    "LIMIT 1", (character_name, potion_id))
    
        potion_id_cp = self._cursor.fetchone()
        
        self._cursor.execute("DELETE FROM characters_potions WHERE id_cp = ?", potion_id_cp)
        
        self.__dungeon_db.commit()

    #-------------------------
    # Gets character's potions 
    #-------------------------
    def get_potions(self, character: Character):
        potions_props = [('id_potion',), ('name',), ('level',), ('stat_rest',), ('amount_rest',)]

        self._cursor.execute("SELECT P.id_potion, P.name, P.level, P.stat_rest, P.amount_rest FROM potions P " +
                        "JOIN characters_potions CP ON P.id_potion = CP.ref_potion " +
                        "WHERE CP.ref_character = ? " +
                        "GROUP BY P.id_potion", (character.name,))
        
        potions_list = self._cursor.fetchall()
        
        self._cursor.execute("SELECT COUNT(P.id_potion) FROM potions P " +
                        "JOIN characters_potions CP ON P.id_potion = CP.ref_potion " +
                        "WHERE CP.ref_character = ? " +
                        "GROUP BY P.id_potion", (character.name,))
        
        potions_count = self._cursor.fetchall()
        
        potions = False
        
        if len(potions_list): 
            potions = self.data_to_dict(potions_props, potions_list)

            for i in range(0, len(potions)):
                potion = Potion(potions[i])
                print(f"{i+1}. {potion.name} x{potions_count[i][0]} | {potion.stat_rest} = {potion.amount_rest}")
                potions[i] = potion

        return potions

    #---------------------------------
    # Compares stats between two items
    #---------------------------------
    def items_comparation(self, character: Character, item):
        item_equipped_post = []
        
        if isinstance(item, Gear):
            self._cursor.execute("SELECT G.id_gear, G.defense, G.dodge FROM gear G " +
                        "JOIN characters_gear CG ON G.id_gear = CG.ref_gear " +
                        "WHERE CG.ref_character = ? AND CG.equipped = TRUE", (character.name,))
            
            item_equipped = self._cursor.fetchone()
            
            if item_equipped:
                defense_var = item.defense - int(item_equipped[1])
                
                if defense_var >= 0 : defense_var = "+" + str(defense_var)
                
                dodge_var = item.dodge - item_equipped[2]
                
                if dodge_var >= 0 : dodge_var = "+" + str(dodge_var)
                
                item_equipped_post = [item_equipped[0], item_equipped[1], item_equipped[2]]
                
            else:
                defense_var = "+" + str(item.defense)
                dodge_var = "+" + str(item.dodge)

            print("----------------------------------------\n"
                f"{item.name} stats\n"
                "----------------------------------------\n"
                f"Class: {item.gear_class}\n"
                f"Defense: {item.defense} ({defense_var})\n"
                f"Dodge: {item.dodge} ({dodge_var})\n"
                "----------------------------------------")

        elif isinstance(item, Weapon):
            self._cursor.execute("SELECT W.id_weapon, W.attack, W.critical_hit FROM weapons W " +
                        "JOIN characters_weapons CW ON W.id_weapon = CW.ref_weapon " +
                        "WHERE CW.ref_character = ? AND CW.equipped = TRUE", (character.name,))
            
            item_equipped = self._cursor.fetchone()
            
            if item_equipped:
                attack_var = item.attack - int(item_equipped[1])
                
                if attack_var >= 0 : attack_var = "+" + str(attack_var)
                
                critical_var = item.critical_hit - item_equipped[2]
                
                if critical_var >= 0 : critical_var = "+" + str(critical_var)
                
                item_equipped_post = [item_equipped[0], item_equipped[1], item_equipped[2]]
                
            else:
                attack_var = "+" + str(item.attack)
                critical_var = "+" + str(item.critical_hit)
                
            print("----------------------------------------\n"
                f"{item.name} stats\n"
                "----------------------------------------\n"
                f"Class: {item.weapon_class}\n"
                f"Attack: {item.attack} ({attack_var})\n"
                f"Critical Hit: {item.critical_hit} ({critical_var})\n"
                "----------------------------------------")
                
        return item_equipped_post

    #------------------------------------------
    # Character equips an item (gear or weapon)
    #------------------------------------------
    def equip_item(self, character: Character, item, item_equipped):
        if isinstance(item, Gear):
            if len(item_equipped):
                self._cursor.execute("UPDATE characters_gear SET equipped = FALSE WHERE ref_character = ? AND ref_gear = ?", (character.name, item_equipped[0]))
                self.__dungeon_db.commit()
                character.defense -= item_equipped[1]
                character.dodge -= item_equipped[2]
                
            self._cursor.execute("UPDATE characters_gear SET equipped = TRUE WHERE ref_character = ? AND ref_gear = ?", (character.name, item.id))
            
            self.__dungeon_db.commit()
            
            character.defense += item.defense
            
            dodge_final = character.dodge + item.dodge
            
            if dodge_final > 100:
                character.dodge = 100
            else:
                character.dodge += item.dodge
            
        elif isinstance(item, Weapon):
            
            if len(item_equipped):
                self._cursor.execute("UPDATE characters_weapons SET equipped = FALSE WHERE ref_character = ? AND ref_weapon = ?", (character.name, item_equipped[0]))
                
                self.__dungeon_db.commit()
                
                character.attack -= item_equipped[1]
                character.critical_hit -= item_equipped[2]
                
            self._cursor.execute("UPDATE characters_weapons SET equipped = TRUE WHERE ref_character = ? AND ref_weapon = ?", (character.name, item.id))
            
            self.__dungeon_db.commit()
            
            character.attack += item.attack
            
            critical_final = character.critical_hit + item.critical_hit
            
            if critical_final > 100:
                character.critical_hit = 100
            else:
                character.critical_hit += item.critical_hit

        print(f"\n{item.name} equipped!")

    #-------------------------------------------------
    # Stores a found item in the character's inventory
    #-------------------------------------------------
    def save_item_in_inventory(self, character: Character, item):
        if isinstance(item, Gear):   
            insert_query = "INSERT INTO characters_gear(id_cg, ref_character, ref_gear, equipped) VALUES(?, ?, ?, ?)"
            values = (self.get_new_id("characters_gear", "id_cg"), character.name, item.id, False)
            
        elif isinstance(item, Weapon):
            insert_query = "INSERT INTO characters_weapons(id_cw, ref_character, ref_weapon, equipped) VALUES(?, ?, ?, ?)"
            values = (self.get_new_id("characters_weapons", "id_cw"), character.name, item.id, False)
            
        elif isinstance(item, Potion):
            insert_query = "INSERT INTO characters_potions(id_cp, ref_character, ref_potion) VALUES(?, ?, ?)"
            values = (self.get_new_id("characters_potions", "id_cp"), character.name, item.id)

        self._cursor.execute(insert_query, values)
        
        self.__dungeon_db.commit()

    #-------------------------
    # Gets monster's abilities
    #-------------------------
    def get_monster_abilities(self, monster_type):
        abilities_props = [('id_ability',), ('name',), ('attack_power',), ('resources_cost',), ('probability',)]
        
        self._cursor.execute("SELECT id_ability, name, attack_power, resources_cost, probability FROM monsters_abilities WHERE ref_monster_type = ?", (monster_type,))
        abilities_list = self._cursor.fetchall()
        
        abilities_dicts = self.data_to_dict(abilities_props, abilities_list)
        
        abilities = [MonsterAbility(ability) for ability in abilities_dicts]
                    
        return abilities
    
    #---------------------------
    # Gets character's abilities
    #---------------------------
    def get_character_abilities(self, character_class, level = 1):
        abilities_props = [('id_ability',), ('name',), ('level',), ('attack_power',), ('resources_cost',)]
        
        self._cursor.execute("SELECT id_ability, name, level, attack_power, resources_cost FROM classes_abilities WHERE ref_class = ? AND level <= ? ORDER BY level", (character_class, level))
        abilities_list = self._cursor.fetchall()
        
        abilities_dicts = self.data_to_dict(abilities_props, abilities_list)
        
        abilities = [CharacterAbility(ability) for ability in abilities_dicts]
            
        return abilities
    
    #----------------------------
    # Opens character's inventory
    #----------------------------
    def open_inventory(self, character_name):
        # -----------------------------
        # GEAR
        # -----------------------------
        
        self._cursor.execute("SELECT G.name FROM gear G "
        "JOIN characters_gear CG ON G.id_gear = CG.ref_gear WHERE CG.ref_character = ?", (character_name,))

        gear_names = self._cursor.fetchall()
        
        print("Gear\n------------------------")
        
        if len(gear_names) > 0:
            for gear in gear_names: print(f"-{gear}")
                
        # -----------------------------
        # WEAPONS
        # -----------------------------

        self._cursor.execute("SELECT W.name FROM weapons W "
        "JOIN characters_weapons CW ON W.id_weapon = CW.ref_weapon WHERE CW.ref_character = ?", (character_name,))

        weapons_names = self._cursor.fetchall()
        
        print("\n------------------------\n"
                "Weapons\n------------------------")
        
        if len(weapons_names) > 0:
            for weapon in weapons_names: print(f"-{weapon}")
            
        # -----------------------------
        # POTIONS
        # -----------------------------

        self._cursor.execute("SELECT P.id_potion, P.name, COUNT(*) FROM potions P "
        "JOIN characters_potions CP ON P.id_potion = CP.ref_potion WHERE CP.ref_character = ? "
        "GROUP BY P.id_potion", (character_name,))

        potions_list = self._cursor.fetchall()
        
        print("\n------------------------\n"
                "Potions\n------------------------")

        if len(potions_list) > 0:
            for potion in potions_list: print(f"{potion[2]}x {potion[1]}")

        print("------------------------")

    #---------------------------------------------
    # Checks whether the character can use an item
    #---------------------------------------------
    def check_inventory_item(self, item_name, item_type, character_name):
        if item_type == "gear":
            self._cursor.execute("SELECT ref_gear FROM characters_gear CG " + 
            "JOIN characters C ON CG.ref_character = C.name " +
            "JOIN gear G ON CG.ref_gear = G.id_gear " +
            "WHERE G.name = ? AND C.name = ?", (item_name, character_name))
        else:
            self._cursor.execute("SELECT ref_weapon FROM characters_weapons CW " + 
            "JOIN characters C ON CW.ref_character = C.name " +
            "JOIN weapons W ON CW.ref_weapon = W.id_weapon " +
            "WHERE W.name = ? AND C.name = ?", (item_name, character_name))

        item = self._cursor.fetchone()
        
        return True if item else False

    #-------------------------------------
    # Gets a random item from a loot chest
    #-------------------------------------
    def get_items(self, floor_level):
        gear_props = [('id_gear',), ('name',), ('class',), ('level',), ('defense',), ('dodge',)]
        weapons_props = [('id_weapon',), ('name',), ('class',), ('level',), ('attack',), ('critical_hit',)]
        potions_props = [('id_potion',), ('name',), ('level',), ('stat_rest',), ('amount_rest',)]
    
        self._cursor.execute("SELECT * FROM gear WHERE level = ?", (floor_level,))
        gear_list = self._cursor.fetchall()
        
        self._cursor.execute("SELECT * FROM weapons WHERE level = ?", (floor_level,))
        weapons_list = self._cursor.fetchall()
        
        self._cursor.execute("SELECT * FROM potions WHERE level = ?", (floor_level,))
        potions_list = self._cursor.fetchall()
        
        items = []
        
        if len(gear_list):
            gear_items = self.data_to_dict(gear_props, gear_list)
            
            for gear in gear_items:
                items.append(Gear(gear))
            
        if len(weapons_list):
            weapon_items = self.data_to_dict(weapons_props, weapons_list)
            
            for weapon in weapon_items:
                items.append(Weapon(weapon))
                
        if len(potions_list):
            potion_items = self.data_to_dict(potions_props, potions_list)
            
            for potion in potion_items:
                items.append(Potion(potion))

        return items
    
    #--------------------
    # Gets floor name
    #--------------------
    def get_floor_name(self, floor_level):
        self._cursor.execute("SELECT name FROM floors WHERE level = ?", (floor_level,))
        floor_name = self._cursor.fetchone()[0]
        
        return floor_name
    
    #-----------------------
    # Gets floor description
    #-----------------------
    def get_floor_description(self, floor_level):
        self._cursor.execute("SELECT description FROM floors WHERE level = ?", (floor_level,))
        floor_description = self._cursor.fetchone()[0]
        
        return floor_description
    
    #--------------------
    # Deletes a character
    #--------------------
    def delete_game(self, character_name):
        self._cursor.execute("DELETE FROM characters WHERE name = ?", (character_name,))
        
        self.__dungeon_db.commit()
        
        print("Game deleted.");

    #------------------------------
    # Gets all the saved characters 
    #------------------------------
    def get_characters(self):
        character_stats = [('name',), ('ref_class',),('level',), ('hp',), ('mp',), ('stamina',), ('strength',), ('agility',), 
                    ('intellect',), ('attack',), ('defense',), ('critical_hit',), ('dodge',), ('luck',), ('ref_floor_level',)]
        
        self._cursor.execute("SELECT * FROM characters")
        characters_data = self._cursor.fetchall()
        
        characters_dict = self.data_to_dict(character_stats, characters_data) if len(characters_data) else []
        characters = []
        
        if (len(characters_dict) > 0):
            for character in characters_dict:
                character_abilities = self.get_character_abilities(character['ref_class'])
                characters.append(Character(character, character_abilities))
        
        return characters
    
    #----------------------------------------------
    # Gets character's stats depending on its class
    #----------------------------------------------
    def get_class_stats(self, character_class):
        class_stats = [('ref_class',), ('hp',), ('mp',), ('stamina',), ('strength',), ('agility',), 
                    ('intellect',), ('attack',), ('defense',), ('critical_hit',), ('dodge',)]
        
        self._cursor.execute("SELECT * FROM classes WHERE name = ?", (character_class,))
        class_data = self._cursor.fetchone()

        return self.data_to_dict(class_stats, class_data)[0]
    
    #------------------------
    # Creates a new character
    #------------------------
    def create_new_character(self, character_class):
        class_stats = [('ref_class',), ('hp',), ('mp',), ('stamina',), ('strength',), ('agility',), 
                    ('intellect',), ('attack',), ('defense',), ('critical_hit',), ('dodge',)]
        
        self._cursor.execute("SELECT * FROM classes WHERE name = ?", (character_class,))
        class_data = self._cursor.fetchone()
        
        class_data_dict = self.data_to_dict(class_stats, class_data)[0]
        
        character_abilities = self.get_character_abilities(class_data_dict['ref_class'])
    
        character = Character(class_data_dict, character_abilities)
            
        return character

    #-----------------------------------------------------
    # Gets monsters with the same level as the floor level
    #-----------------------------------------------------
    def get_level_monsters(self, level):
        monster_stats = [('monster_type',), ('level',), ('hp',), ('mp',), ('stamina',), ('strength',), ('agility',), 
                        ('intellect',), ('attack',), ('defense',), ('critical_hit',), ('dodge',)]
            
        self._cursor.execute("SELECT * FROM monsters WHERE level = ?", (level,))
        monsters_data = self._cursor.fetchall()
            
        monsters_data_dict = self.data_to_dict(monster_stats, monsters_data)
        
        monsters = [Monster(monster, self.get_monster_abilities(monster['monster_type'])) for monster in monsters_data_dict]
        
        return monsters
    
    #--------------
    # Gets THE BOSS
    #--------------
    def get_black_dragon(self):
        monster_stats = [('monster_type',), ('level',), ('hp',), ('mp',), ('stamina',), ('strength',), ('agility',), 
                        ('intellect',), ('attack',), ('defense',), ('critical_hit',), ('dodge',)]
        
        self._cursor.execute("SELECT * FROM monsters WHERE monster_type = 'Black Dragon'")
        monster_data = self._cursor.fetchone()
            
        monsters_data_dict = self.data_to_dict(monster_stats, monster_data)
        
        return Monster(monsters_data_dict[0], self.get_monster_abilities(monsters_data_dict[0]['monster_type']))
    
    #--------------------------------
    # Saves character in the database
    #--------------------------------
    def save_character(self, character: Character):
        insert_query = "INSERT INTO characters VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        values = (character.name, character.character_class,
        character.level, character.hp, character.mp, character.stamina, character.strength, character.agility,
        character.intellect, character.attack, character.defense,
        character.critical_hit, character.dodge, character.luck, character.floor_level)

        self._cursor.execute(insert_query, values)
        
        self.__dungeon_db.commit()

    #-------------------------------------------------------
    # Checks if there's another character with the same name
    #-------------------------------------------------------         
    def check_new_character_name(self, name):
        self._cursor.execute("SELECT name FROM characters WHERE name = ?", (name,))
        name_exists = self._cursor.fetchone()
        
        return True if name_exists else False
    
    #---------------------------------------------------------------------
    # Transforms the raw data obtained from the database into a dictionary
    #---------------------------------------------------------------------
    def data_to_dict(self, stats, data_tuples):
        data_array = []
        
        count_data = -1
           
        if isinstance(data_tuples[0], tuple):
            for data_tuple in data_tuples:
                count_tuple = 0
                count_data += 1
                data_array.append(stats.copy())

                for data in data_tuple:
                    data_array[count_data][count_tuple] += (data,)
                    count_tuple += 1
                    
        else:
            count_tuple = 0
            data_array.append(stats.copy())
            
            for data in data_tuples:
                data_array[0][count_tuple] += (data,)
                count_tuple += 1
        
        data_array = [dict(data) for data in data_array]
                    
        return data_array
    
    def get_new_id(self, table, id_col):
        self._cursor.execute(f"SELECT MAX({id_col}) FROM {table}")
        id_max = self._cursor.fetchone()[0]
        
        if id_max:
            id_max += 1
        else:
            id_max = 1
            
        return id_max
        