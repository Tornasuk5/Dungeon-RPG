from numpy import *

from database.PoolCursor import PoolCursor

from components.items.Potion import Potion
from components.items.Gear import Gear
from components.items.Weapon import Weapon
from components.models.Character import Character
from components.models.Monster import Monster
from components.abilities.CharacterAbility import CharacterAbility
from components.abilities.MonsterAbility import MonsterAbility

class RPGDAO:
    #-----------------------------------------------------
    # Saves (modifies) character's stats into the database
    #-----------------------------------------------------
    @staticmethod
    def auto_save_game(character: Character):
        with PoolCursor() as cursor:
            update_query = "UPDATE characters SET level = %s, hp = %s, mp = %s, stamina = %s, strength = %s, agility = %s, intellect = %s, attack = %s, defense = %s, critical_hit = %s, dodge = %s, luck = %s, ref_floor_level = %s WHERE name = %s"
            
            values = (character.level, character.hp, character.mp, character.stamina, character.strength, 
                        character.agility, character.intellect, character.attack, character.defense,
                        character.critical_hit, character.dodge, character.luck, character.floor_level, character.name)

            cursor.execute(update_query, values)
            
    #-------------------------------------------
    # Character consumes a potion from inventory
    #-------------------------------------------
    @staticmethod
    def use_potion(character_name, potion: Potion, rest):
            with PoolCursor() as cursor:
                cursor.execute("DELETE FROM characters_potions WHERE ref_character = %s AND ref_potion = %s", (character_name, potion.id))
                
                print(f"You drink '{potion.name}' and restores +{rest} {potion.stat_rest}")

    #-------------------------
    # Gets character's potions 
    #-------------------------
    @classmethod
    def get_potions(cls, character: Character):
        with PoolCursor() as cursor:
            potions_props = [('id_potion',), ('name',), ('level',), ('stat_rest',), ('amount_rest',)]

            cursor.execute("SELECT P.id_potion, P.name, P.level, P.stat_rest, P.amount_rest FROM potions P " +
                            "JOIN characters_potions CP ON P.id_potion = CP.ref_potion " +
                            "WHERE CP.ref_character = %s " +
                            "GROUP BY P.id_potion", (character.name,))
            
            potions_list = cursor.fetchall()
            
            cursor.execute("SELECT COUNT(P.id_potion) FROM potions P " +
                            "JOIN characters_potions CP ON P.id_potion = CP.ref_potion " +
                            "WHERE CP.ref_character = %s " +
                            "GROUP BY P.id_potion", (character.name,))
            
            potions_count = cursor.fetchall()
            
            potions = False
            
            if len(potions_list): 
                potions = cls.data_to_dict(potions_props, potions_list)

                for i in range(0, len(potions)):
                    potion = Potion(potions[i])
                    print(f"{i+1}. {potion.name} x{potions_count[i][0]} | {potion.stat_rest} = {potion.amount_rest}")
                    potions[i] = potion

        return potions

    #---------------------------------
    # Compares stats between two items
    #---------------------------------
    @staticmethod
    def items_comparation(character: Character, item):
        with PoolCursor() as cursor:
            item_equipped_post = []
            
            if isinstance(item, Gear):
                cursor.execute("SELECT G.id_gear, G.defense, G.dodge FROM gear G " +
                            "JOIN characters_gear CG ON G.id_gear = CG.ref_gear " +
                            "WHERE CG.ref_character = %s AND CG.equipped = TRUE", (character.name,))
                
                item_equipped = cursor.fetchone()
                
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
                cursor.execute("SELECT W.id_weapon, W.attack, W.critical_hit FROM weapons W " +
                            "JOIN characters_weapons CW ON W.id_weapon = CW.ref_weapon " +
                            "WHERE CW.ref_character = %s AND CW.equipped = TRUE", (character.name,))
                
                item_equipped = cursor.fetchone()
                
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
    @staticmethod
    def equip_item(character: Character, item, item_equipped):
            with PoolCursor() as cursor:
                if isinstance(item, Gear):
                    
                    if len(item_equipped):
                        cursor.execute("UPDATE characters_gear SET equipped = FALSE WHERE ref_character = %s AND ref_gear = %s", (character.name, item_equipped[0]))
                        character.defense -= item_equipped[1]
                        character.dodge -= item_equipped[2]
                        
                    cursor.execute("UPDATE characters_gear SET equipped = TRUE WHERE ref_character = %s AND ref_gear = %s", (character.name, item.id))
                    character.defense += item.defense
                    character.dodge += item.dodge
                    
                elif isinstance(item, Weapon):
                    
                    if len(item_equipped):
                        cursor.execute("UPDATE characters_weapons SET equipped = FALSE WHERE ref_character = %s AND ref_weapon = %s", (character.name, item_equipped[0]))
                        character.attack -= item_equipped[1]
                        character.critical_hit -= item_equipped[2]
                        
                    cursor.execute("UPDATE characters_weapons SET equipped = TRUE WHERE ref_character = %s AND ref_weapon = %s", (character.name, item.id))
                    character.attack += item.attack
                    character.critical_hit += item.critical_hit

                print(f"{item.name} equipped!")

    #-------------------------------------------------
    # Stores a found item in the character's inventory
    #-------------------------------------------------
    @staticmethod
    def save_item_in_inventory(character: Character, item):
            with PoolCursor() as cursor:
                if isinstance(item, Gear):
                    insert_query = "INSERT INTO characters_gear(ref_character, ref_gear, equipped) VALUES(%s, %s, %s)"
                    values = (character.name, item.id, False)
                    
                elif isinstance(item, Weapon):
                    insert_query = "INSERT INTO characters_weapons(ref_character, ref_weapon, equipped) VALUES(%s, %s, %s)"
                    values = (character.name, item.id, False)
                    
                elif isinstance(item, Potion):
                    insert_query = "INSERT INTO characters_potions(ref_character, ref_potion) VALUES(%s, %s)"
                    values = (character.name, item.id)

                cursor.execute(insert_query, values)

    #-------------------------
    # Gets monster's abilities
    #-------------------------
    @classmethod
    def get_monster_abilities(cls, monster_type):
        with PoolCursor() as cursor:
            abilities_props = [('id_ability',), ('name',), ('attack_power',), ('resources_cost',), ('probability',)]
            
            cursor.execute("SELECT id_ability, name, attack_power, resources_cost, probability FROM monsters_abilities WHERE ref_monster_type = %s", (monster_type,))
            abilities_list = cursor.fetchall()
            
            abilities_dicts = cls.data_to_dict(abilities_props, abilities_list)
            
            abilities = []
        
        for ability in abilities_dicts:
            ability = MonsterAbility(ability)
            abilities.append(ability)
                    
        return abilities
    
    #---------------------------
    # Gets character's abilities
    #---------------------------
    @classmethod
    def get_character_abilities(cls, character_class, level = 1):
        with PoolCursor() as cursor:
            abilities_props = [('id_ability',), ('name',), ('level',), ('attack_power',), ('resources_cost',)]
            
            cursor.execute("SELECT id_ability, name, level, attack_power, resources_cost FROM classes_abilities WHERE ref_class = %s AND level <= %s", (character_class, level))
            abilities_list = cursor.fetchall()
            
            abilities_dicts = cls.data_to_dict(abilities_props, abilities_list)
            
            abilities = []
        
        for ability in abilities_dicts:
            ability = CharacterAbility(ability)
            abilities.append(ability)
            
        return abilities
    
    #----------------------------
    # Opens character's inventory
    #----------------------------
    @staticmethod
    def open_inventory(character_name):
        with PoolCursor() as cursor:
        
            # -----------------------------
            # GEAR
            # -----------------------------
            
            cursor.execute("SELECT G.name FROM gear G "
            "JOIN characters_gear CG ON G.id_gear = CG.ref_gear WHERE CG.ref_character = %s", (character_name,))

            gear_names = cursor.fetchall()
            
            print("Gear\n------------------------")
            
            if len(gear_names) > 0:
                for gear in gear_names: print(f"-{gear}")
                    
            # -----------------------------
            # WEAPONS
            # -----------------------------

            cursor.execute("SELECT W.name FROM weapons W "
            "JOIN characters_weapons CW ON W.id_weapon = CW.ref_weapon WHERE CW.ref_character = %s", (character_name,))

            weapons_names = cursor.fetchall()
            
            print("\n------------------------\n"
                  "Weapons\n------------------------")
            
            if len(weapons_names) > 0:
                for weapon in weapons_names: print(f"-{weapon}")
                
            # -----------------------------
            # POTIONS
            # -----------------------------

            cursor.execute("SELECT P.id_potion, P.name, COUNT(*) FROM potions P "
            "JOIN characters_potions CP ON P.id_potion = CP.ref_potion WHERE CP.ref_character = %s "
            "GROUP BY P.id_potion", (character_name,))

            potions_list = cursor.fetchall()
            
            print("\n------------------------\n"
                  "Potions\n------------------------")

            if len(potions_list) > 0:
                for potion in potions_list: print(f"{potion[2]}x {potion[1]}")

            print("------------------------")

    #---------------------------------------------
    # Checks whether the character can use an item
    #---------------------------------------------
    @staticmethod
    def check_inventory_item(item_name, item_type, character_name):
        with PoolCursor() as cursor:
        
            if item_type == "gear":
                cursor.execute("SELECT ref_gear FROM characters_gear CG " + 
                "JOIN characters C ON CG.ref_character = C.name " +
                "JOIN gear G ON CG.ref_gear = G.id_gear " +
                "WHERE G.name = %s AND C.name = %s", (item_name, character_name))
            else:
                cursor.execute("SELECT ref_weapon FROM characters_weapons CW " + 
                "JOIN characters C ON CW.ref_character = C.name " +
                "JOIN weapons W ON CW.ref_weapon = W.id_weapon " +
                "WHERE W.name = %s AND C.name = %s", (item_name, character_name))

            item = cursor.fetchone()
        
        return True if item else False

    #-------------------------------------
    # Gets a random item from a loot chest
    #-------------------------------------
    @classmethod
    def get_items(cls, floor_level):
        with PoolCursor() as cursor:
            
            gear_props = [('id_gear',), ('name',), ('class',), ('level',), ('defense',), ('dodge',)]
            weapons_props = [('id_weapon',), ('name',), ('class',), ('level',), ('attack',), ('critical_hit',)]
            potions_props = [('id_potion',), ('name',), ('level',), ('stat_rest',), ('amount_rest',)]
        
            cursor.execute("SELECT * FROM gear WHERE level <= %s", (floor_level,))
            gear_list = cursor.fetchall()
            
            cursor.execute("SELECT * FROM weapons WHERE level <= %s", (floor_level,))
            weapons_list = cursor.fetchall()
            
            cursor.execute("SELECT * FROM potions WHERE level <= %s", (floor_level,))
            potions_list = cursor.fetchall()
            
            items = []
            
            if len(gear_list):
                gear_items = cls.data_to_dict(gear_props, gear_list)
                for i in range(0, len(gear_items)):
                    gear_obj = Gear(gear_items[i])
                    items.append(gear_obj)
                
            if len(weapons_list):
                weapon_items = cls.data_to_dict(weapons_props, weapons_list)
                for i in range(0, len(weapon_items)):
                    weapon_obj = Weapon(weapon_items[i])
                    items.append(weapon_obj)
                
            if len(potions_list):
                potion_items = cls.data_to_dict(potions_props, potions_list)
                for i in range(0, len(potion_items)):
                    potion_obj = Potion(potion_items[i])
                    items.append(potion_obj)

        return items
    
    #--------------------
    # Gets floor name
    #--------------------
    @staticmethod
    def get_floor_name(floor_level):
        with PoolCursor() as cursor:
            cursor.execute("SELECT name FROM floors WHERE level = %s", (floor_level,))
            floor_name = cursor.fetchone()[0]
        
        return floor_name
    
    #-----------------------
    # Gets floor description
    #-----------------------
    @staticmethod
    def get_floor_description(floor_level):
        with PoolCursor() as cursor:
            cursor.execute("SELECT description FROM floors WHERE level = %s", (floor_level,))
            floor_description = cursor.fetchone()[0]
        
        return floor_description
    
    #--------------------
    # Deletes a character
    #--------------------
    @staticmethod
    def delete_game(character_name):
            with PoolCursor() as cursor:
                cursor.execute("DELETE FROM characters WHERE name = %s", (character_name,))
                print("Game deleted.");

    #------------------------------
    # Gets all the saved characters 
    #------------------------------
    @classmethod
    def get_characters(cls):
        with PoolCursor() as cursor:
            character_stats = [('name',), ('ref_class',),('level',), ('hp',), ('mp',), ('stamina',), ('strength',), ('agility',), 
                        ('intellect',), ('attack',), ('defense',), ('critical_hit',), ('dodge',), ('luck',), ('ref_floor_level',)]
            
            cursor.execute("SELECT * FROM characters")
            characters_data = cursor.fetchall()
            
            characters_dict = cls.data_to_dict(character_stats, characters_data) if len(characters_data) else []
            characters = []
            
            if (len(characters_dict) > 0):
                for character in characters_dict:
                    character_abilities = cls.get_character_abilities(character['ref_class'])
                    characters.append(Character(character, character_abilities))
        
        return characters
    
    
    #----------------------------------------------
    # Gets character's stats depending on its class
    #----------------------------------------------
    @classmethod
    def get_class_stats(cls, character_class):
        with PoolCursor() as cursor:
            class_stats = [('ref_class',), ('hp',), ('mp',), ('stamina',), ('strength',), ('agility',), 
                        ('intellect',), ('attack',), ('defense',), ('critical_hit',), ('dodge',)]
            
            cursor.execute("SELECT * FROM classes WHERE name = %s", (character_class,))
            class_data = cursor.fetchone()

        return cls.data_to_dict(class_stats, class_data)[0]
    
    #------------------------
    # Creates a new character
    #------------------------
    @classmethod
    def create_new_character(cls, character_class):
        with PoolCursor() as cursor:
            class_stats = [('ref_class',), ('hp',), ('mp',), ('stamina',), ('strength',), ('agility',), 
                        ('intellect',), ('attack',), ('defense',), ('critical_hit',), ('dodge',)]
            
            cursor.execute("SELECT * FROM classes WHERE name = %s", (character_class,))
            class_data = cursor.fetchone()
            
            class_data_dict = cls.data_to_dict(class_stats, class_data)[0]
            
            character_abilities = cls.get_character_abilities(class_data_dict['ref_class'])
        
            character = Character(class_data_dict, character_abilities)
            
        return character

    #-----------------------------------------------------
    # Gets monsters with the same level as the floor level
    #-----------------------------------------------------
    @classmethod
    def get_level_monsters(cls, level):
        monster_stats = [('monster_type',), ('level',), ('hp',), ('mp',), ('stamina',), ('strength',), ('agility',), 
                        ('intellect',), ('attack',), ('defense',), ('critical_hit',), ('dodge',)]
        
        with PoolCursor() as cursor:
            
            cursor.execute("SELECT * FROM monsters WHERE level = %s", (level,))
            monsters_data = cursor.fetchall()
            
        monsters_data_dict = cls.data_to_dict(monster_stats, monsters_data)
        
        monsters = []
                 
        for monster in monsters_data_dict:
            monsters.append(Monster(monster, cls.get_monster_abilities(monster['monster_type'])))
        
        return monsters
    
    #--------------------------------
    # Saves character in the database
    #--------------------------------
    @staticmethod
    def save_character(character: Character):
            with PoolCursor() as cursor:
        
                insert_query = "INSERT INTO characters VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (character.name, character.character_class,
                character.level, character.hp, character.mp, character.stamina, character.strength, character.agility,
                character.intellect, character.attack, character.defense,
                character.critical_hit, character.dodge, character.luck, character.floor_level)

                cursor.execute(insert_query, values)

    #-------------------------------------------------------
    # Checks if there's another character with the same name
    #-------------------------------------------------------   
    @staticmethod        
    def check_new_character_name(name):
        with PoolCursor() as cursor:
            cursor.execute("SELECT name FROM characters WHERE name = %s", (name,))
            name_exists = cursor.fetchone()
        
        return True if name_exists else False
    
    #---------------------------------------------------------------------
    # Transforms the raw data obtained from the database into a dictionary
    #---------------------------------------------------------------------
    @classmethod
    def data_to_dict(cls, stats, data_tuples):
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
                
        for i in range(0, len(data_array)):
            data_dict = dict(data_array[i])
            data_array[i] = data_dict
            
        return data_array