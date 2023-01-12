import math
import time
import random
from components.items.Gear import Gear
from components.items.Potion import Potion
from components.items.Weapon import Weapon
from components.models.Monster import Monster
from utils.GameMethods import print_game_delay, exit_game, check_option


def start_game(floor): 
    print_game_delay("Starting game...")
    print_game_delay(f"Level {floor.level} - {floor.name}")
    
#----------------------
# Shows the battle flow
#----------------------
def battle(run_data, monster):
    character = run_data.character
        
    print_game_delay(f"{monster.monster_type} appears!")

    while monster.hp > 0 and character.hp > 0:
        if monster.monster_type != "Mimic":
            prob_monster_ability_random = random.randint(1, 100)
            
            if prob_monster_ability_random <= run_data.PROB_MONSTER_ABILITY:
                monster_abilities = monster.abilities
                
                if len(monster_abilities):
                    prob_ability = random.randint(1, 100)

                    if prob_ability <= monster_abilities[1].probability: 
                        ability = monster_abilities[1]
                    else: 
                        ability = monster_abilities[0]
                    
                    if monster.get_main_resource() >= ability.resources_cost: 
                        monster.monster_ability(ability, character)
                    else: 
                        monster.monster_attack(character)
                    
            else: monster.monster_attack(character)
            
        else: monster.monster_attack(character)

        if character.hp > 0:
            character_battle_menu(run_data, monster)           

    if monster.hp <= 0: 
        print_game_delay(f"{character.name} has defeated a {monster.monster_type} (level {monster.level})")
        del monster
    else:
        print_game_delay("You are dead.")
        run_data.db_manager.rpgdao.delete_game(character.name)
        exit_game()
            
    
# -------------------------------------------------------------------
# Shows an "encounter with a loot chest (or something else...)" event
# -------------------------------------------------------------------
def loot_encounter(run_data):
    character = run_data.character
    
    print("\nYou have encountered a chest!")
    op = input("Do you want to open it? (Y / N) -> ")
    
    if op.lower() == 'y':
        
        if random.randint(1, 100) <= run_data.PROB_TRAP:
            
            print_game_delay("The chest is a TRAP!")
            
            trap_list = ["poison", "mimic", "explosion"]
            random_trap = random.choice(trap_list)

            if random_trap == "poison":
                damage = int(character.get_full_hp() * 0.1)
                character.hp = character.hp - damage
                print_game_delay(f"You have been poisoned! -> You receive {damage} damage")
                
            elif random_trap == "mimic":
                level = run_data.floor.level
                mimic = Monster({
                                "monster_type": "Mimic",
                                "level": level,
                                "hp": (4 * level) + math.ceil((4 * level) * level * 0.3),
                                "mp": 0,
                                "stamina": 0,
                                "strength": level,
                                "agility": 0,
                                "intellect": 0,
                                "attack": level + math.ceil(level * 0.3),
                                "defense": 0,
                                "critical_hit": 0,
                                "dodge": 0
                                }, [])
                battle(run_data, mimic)

            elif random_trap == "explosion":
                damage = int(character.get_full_hp() * 0.25)
                character.hp = character.hp - damage
                print_game_delay(f"The chest has exploted! -> You receive {damage} damage")
                
            # Character's life's under 0 HP (DEAD)
            if character.hp <= 0:
                print_game_delay("You are dead.")
                run_data.db_manager.rpgdao.delete_game(character.name)
                exit_game()
                
        else:
            items = run_data.db_manager.rpgdao.get_items(run_data.floor.level)
            item = random.choice(items) # Picks a random item
            
            print_game_delay("You open the chest and...")
            
            print(f"You get '{item.name}'!")
            time.sleep(1)

            # Item type -> Gear
            if isinstance(item, Gear):
                
                if item.gear_class == character.character_class: # Checks gear's compatibility
                    
                    if run_data.db_manager.rpgdao.check_inventory_item(item.name, "gear", character.name): # Checks whether the gear is in inventory or not
                        print("...but you already have this item.")
                    else:
                        run_data.db_manager.rpgdao.save_item_in_inventory(character, item)
                        item_equipped = run_data.db_manager.rpgdao.items_comparation(character, item) # Gear comparation between the getted and the equipped one
                        
                        op = input("Do you want to equip it? (Y / N) -> ")
                        
                        if op.lower() == 'y': run_data.db_manager.rpgdao.equip_item(character, item, item_equipped) # Equips gear
                            
                else: 
                    print("...but you can't use this item")
                
            # Item type -> Weapon
            elif isinstance(item, Weapon):  # Item type -> Gear
                
                if item.weapon_class == character.character_class: # Checks weapon's compatibility
                    
                    if run_data.db_manager.rpgdao.check_inventory_item(item.name, "weapon", character.name): # Checks whether the weapon is in inventory or not
                        print("...but you already have this item.")
                    else:
                        run_data.db_manager.rpgdao.save_item_in_inventory(character, item)
                        item_equipped = run_data.db_manager.rpgdao.items_comparation(character, item) # Weapon comparation between the getted and the equipped one
                        
                        op = input("Do you want to equip it? (Y / N) -> ")
                        
                        if op.lower() == 'y': run_data.db_manager.rpgdao.equip_item(character, item, item_equipped) # Equips weapon
                            
                else: 
                    print("...but you can't use this item")

            # Item type -> Potion
            elif isinstance(item, Potion):
                
                if item.stat_rest == "HP" or (item.stat_rest == "MP" and character.character_class == "Mage") or (item.stat_rest == "Stamina" and character.character_class != "Mage"):
                    run_data.db_manager.rpgdao.save_item_in_inventory(character, item)
                    
                else: 
                    print("...but you can't use this item")
                    
    else: 
        print("\nYou decide not to open the chest, it could be a trap...")
    

# -----------------------------------------------------
# Recovers HP, MP and Stamina (+ random stats benefits)
# -----------------------------------------------------
def rest(character):
    print("\nYou've found a place that looks safe")
    op = input("You want to rest a bit before continue? (Y / N) -> ")
    
    if op.lower() == "y":
        amount_hp_rest = int(character.get_full_hp() * 0.2)
        rest_hp = character.hp + amount_hp_rest;
        
        if rest_hp > character.get_full_hp(): 
            amount_hp_rest = character.get_full_hp() - character.hp
            rest_hp = character.get_full_hp()
            
        character.hp = rest_hp
        
        if character.character_class == "Mage":
            
            amount_mp_rest = int(character.get_full_mp() * 0.5)
            rest_mp = character.mp + amount_mp_rest;
            
            if rest_mp > character.get_full_mp(): 
                amount_mp_rest = character.get_full_mp() - character.mp
                rest_mp = character.get_full_mp()
                
            character.mp = rest_mp
            
            print_game_delay(f"After rest, you have recover +{amount_hp_rest} HP and +{amount_mp_rest} MP")
            
        else:
            amount_stamina_rest = int(character.get_full_stamina() * 0.5)
            rest_stamina = character.stamina + amount_stamina_rest;
            
            if rest_stamina > character.get_full_stamina(): 
                amount_stamina_rest = character.get_full_stamina() - character.stamina
                rest_stamina = character.get_full_stamina()
                
            character.stamina = rest_stamina
            
            print(f"\nAfter rest, you have recover +{amount_hp_rest} HP and +{amount_stamina_rest} Stamina")
            
# -------------------------------------------------------------------------
# Prints the 'interface' of the character's options when fighting a monster
# -------------------------------------------------------------------------
def character_battle_menu(run_data, monster):
    character = run_data.character
    print("\n-------------------------------------------------\n"
        f"{monster.monster_type} - HP = {monster.hp} | MP = {monster.mp} | Stamina = {monster.stamina}\n"
        "-------------------------------------------------\n"
        f"{character.name} - HP = {character.hp} | MP = {character.mp} | Stamina = {character.stamina}\n"
        "-------------------------------------------------\n"
        "Actions\n"
        "-------------------------------------------------\n"
        "1. Attack\n"
        "2. Use ability\n"
        "3. Use item")
    
    op = check_option(3)
    
    if op == '1': 
        character.character_attack(monster)
    
    elif op == '2':
        character_abilities = character.abilities
        count = 0
        
        print("------------------------------------------\n"
            f"{character.name} abilities\n"
            "------------------------------------------")
        
        for ability in character_abilities:
            count += 1
            print(f"{count}. {ability.name} - Power: {ability.attack_power} | MP: {ability.resources_cost}")
            
        op = check_option(count, ['b'])
        
        if op == 'b': 
            character_battle_menu(run_data, monster)
        
        elif character.get_main_resource() >= character_abilities[int(op) - 1].resources_cost: # Character have enough resources to cast the ability
            character.character_ability(character_abilities[int(op) - 1], monster)         
        else:
            print_game_delay("Not enough resources")
            character_battle_menu(run_data, monster)
            
    elif op == '3':
        potions = run_data.db_manager.rpgdao.get_potions(character)
        
        if potions:
            op = check_option(len(potions), ['b'])
            
            if op == 'b': 
                character_battle_menu(run_data, monster)
            else:
                potion = potions[int(op) - 1]
                character.consume_potion(potion)
                run_data.db_manager.rpgdao.use_potion(character.name, potion, potion.amount_rest)
        else:
            print_game_delay("No items available.")
            character_battle_menu(run_data, monster)