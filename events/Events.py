import math
import time
import random
from components.items.gear import Gear
from components.items.potion import Potion
from components.items.weapon import Weapon
from components.models.monster import Monster
from utils.game_methods import print_game_delay, exit_game, check_option

#------------------
# Prints event text
#------------------
def print_event(*texts):
    for text in texts:
        if len(text) > 70:
            text_lines = text.split(". ")
            for text_line in text_lines:
                print(f"{text_line}.")
                time.sleep(1)
            time.sleep(1)
        else:
            print_game_delay(text)
            
#----------------------
# Shows the battle flow
#----------------------
def battle(run_data, monster):
    character = run_data.character
        
    print_game_delay(f"{monster.monster_type} appears!")

    while monster.hp > 0 and character.hp > 0:
        if monster.monster_type != "Mimic":
            event_monster = run_data.get_random_choice("monster")
            
            if event_monster == "ability":
                ability = monster.get_random_ability()
                if monster.get_main_resource("monster") >= ability.resources_cost: 
                    monster.monster_ability(ability, character)
            else:
                monster.monster_attack(character)
        else:
            monster.monster_attack(character)

        if character.hp > 0:
            character_battle_menu(run_data, monster)           

    if monster.hp <= 0: 
        print_game_delay(f"{character.name} has defeated a {monster.monster_type} (level {monster.level})")
        del monster
    else:
        print_game_delay("You are dead.")
        run_data.rpgdao.delete_game(character.name)
        exit_game()
            
    
# -------------------------------------------------------------------
# Shows an "encounter with a loot chest (or something else...)" event
# -------------------------------------------------------------------
def loot_encounter(run_data):
    character = run_data.character
    
    print("\nYou have encountered a chest!")
    op = input("Do you want to open it? (Y / N) -> ")
    
    if op.lower() == 'y':
        
        event_loot = run_data.get_random_choice("loot")
        
        if event_loot == "trap":
            
            print_game_delay("The chest is a TRAP!")
            
            trap_events = ["poison", "mimic", "explosion"]
            random_trap = random.choice(trap_events)

            if random_trap == "poison":
                damage = round(character.get_full_hp() * 0.1)
                character.hp -= damage
                print_game_delay(f"You have been poisoned! -> You receive {damage} damage")
                
            elif random_trap == "mimic":
                level = run_data.floor.level
                mimic = Monster({
                                "monster_type": "Mimic",
                                "level": level,
                                "hp": (3 * level) + math.ceil((3 * level) * level * 0.3),
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
                damage = round(character.get_full_hp() * 0.25)
                character.hp -= damage
                print_game_delay(f"The chest has exploted! -> You receive {damage} damage")
                
            # Character's life's under 0 HP (DEAD)
            if character.hp <= 0:
                print_game_delay("You are dead.")
                run_data.rpgdao.delete_game(character.name)
                exit_game()
                
        else:
            items = run_data.rpgdao.get_items(run_data.floor.level)
        
            chest_item = random.choice(items)
            
            print_game_delay("You open the chest and...")
            
            print(f"You get '{chest_item.name}'!")
            time.sleep(1)

            # Item type -> Gear
            if isinstance(chest_item, Gear):
                
                if chest_item.gear_class == character.character_class: # Checks gear's compatibility
                    
                    if run_data.rpgdao.check_inventory_item(chest_item.name, "gear", character.name): # Checks whether the gear is in inventory or not
                        print("...but you already have this item.")
                    else:
                        run_data.rpgdao.save_item_in_inventory(character, chest_item)
                        item_equipped = run_data.rpgdao.items_comparation(character, chest_item) # Gear comparation between the getted and the equipped one
                        
                        op = input("Do you want to equip it? (Y / N) -> ")
                        
                        if op.lower() == 'y': run_data.rpgdao.equip_item(character, chest_item, item_equipped) # Equips gear
                            
                else: 
                    print("...but you can't use this item")
                
            # Item type -> Weapon
            elif isinstance(chest_item, Weapon):  # Item type -> Gear
                
                if chest_item.weapon_class == character.character_class: # Checks weapon's compatibility
                    
                    if run_data.rpgdao.check_inventory_item(chest_item.name, "weapon", character.name): # Checks whether the weapon is in inventory or not
                        print("...but you already have this item.")
                    else:
                        run_data.rpgdao.save_item_in_inventory(character, chest_item)
                        item_equipped = run_data.rpgdao.items_comparation(character, chest_item) # Weapon comparation between the getted and the equipped one
                        
                        op = input("Do you want to equip it? (Y / N) -> ")
                        
                        if op.lower() == 'y': run_data.rpgdao.equip_item(character, chest_item, item_equipped) # Equips weapon
                            
                else: 
                    print("...but you can't use this item")

            # Item type -> Potion
            elif isinstance(chest_item, Potion):
                
                if chest_item.stat_rest == "HP" or (chest_item.stat_rest == "MP" and character.character_class == "Mage") or (chest_item.stat_rest == "Stamina" and character.character_class != "Mage"):
                    run_data.rpgdao.save_item_in_inventory(character, chest_item)
                    
                else: 
                    print("...but you can't use this item")
                    
    else: 
        print("\nYou decide not to open the chest, it could be a trap...")
        
    time.sleep(1)
    

# -----------------------------------------------------
# Recovers HP, MP and Stamina (+ random stats benefits)
# -----------------------------------------------------
def rest(character):
    print("\nYou have found a place that looks safe")
    op = input("You want to rest a bit before continuing? (Y / N) -> ")
    
    if op.lower() == "y":
        amount_hp_rest = int(character.get_full_hp() * 0.2)
        rest_hp = character.hp + amount_hp_rest
        
        if rest_hp > character.get_full_hp(): 
            amount_hp_rest = character.get_full_hp() - character.hp
            rest_hp = character.get_full_hp()
            
        character.hp = rest_hp
        
        if character.character_class == "Mage":
            
            amount_mp_rest = int(character.get_full_mp() * 0.5)
            rest_mp = character.mp + amount_mp_rest
            
            if rest_mp > character.get_full_mp(): 
                amount_mp_rest = character.get_full_mp() - character.mp
                rest_mp = character.get_full_mp()
                
            character.mp = rest_mp
            
            print_game_delay(f"After resting, you recover +{amount_hp_rest} HP and +{amount_mp_rest} MP")
            
        else:
            amount_stamina_rest = int(character.get_full_stamina() * 0.5)
            rest_stamina = character.stamina + amount_stamina_rest
            
            if rest_stamina > character.get_full_stamina(): 
                amount_stamina_rest = character.get_full_stamina() - character.stamina
                rest_stamina = character.get_full_stamina()
                
            character.stamina = rest_stamina
            
            print(f"\nAfter resting, you recover +{amount_hp_rest} HP and +{amount_stamina_rest} Stamina")
            
    time.sleep(1)
            
# -------------------------------------------------------------------------
# Prints the 'interface' of the character's options when fighting a monster
# -------------------------------------------------------------------------
def character_battle_menu(run_data, monster):
    character = run_data.character
    print("\n-------------------------------------------------------------------------------\n"
        f"{monster.monster_type} - HP = {monster.hp} | MP = {monster.mp} | Stamina = {monster.stamina} | Attack = {monster.attack} | Defense = {monster.defense}\n"
        "-------------------------------------------------------------------------------\n"
        f"{character.name} - HP = {character.hp} | MP = {character.mp} | Stamina = {character.stamina} | Attack = {character.attack} | Defense = {character.defense}\n"
        "-------------------------------------------------------------------------------\n"
        "Actions\n"
        "-------------------------------------------------------------------------------\n"
        "1. Attack\n"
        "2. Use ability\n"
        "3. Use item")
    
    op = check_option(3)
    
    if op == '1': 
        character.character_attack(monster)
    
    elif op == '2':
        character_abilities = character.abilities
        count = 0
        
        print("-----------------------------------------------\n"
             f"{character.name} abilities\n"
              "-----------------------------------------------")
        
        for ability in character_abilities:
            count += 1
            print(f"{count}. {ability.name} - Power: {math.ceil(ability.attack_power * character.ability_power)} | {character.get_class_main_resource()} cost: {ability.resources_cost - math.floor(ability.resources_cost * character.ability_save)}")
            
        op = check_option(count, ['b'])
        
        if op == 'b': 
            character_battle_menu(run_data, monster)
        
        elif character.get_main_resource("character") >= (character_abilities[int(op) - 1].resources_cost - math.floor((character_abilities[int(op) - 1].resources_cost * character.ability_save))): # Character have enough resources to cast the ability
            character.character_ability(character_abilities[int(op) - 1], monster)      
        else:
            print_game_delay("Not enough resources")
            character_battle_menu(run_data, monster)
            
    elif op == '3':
        potions = run_data.rpgdao.get_potions(character)
        
        if potions:
            op = check_option(len(potions), ['b'])
            
            if op == 'b': 
                character_battle_menu(run_data, monster)
            else:
                potion = potions[int(op) - 1]
                character.consume_potion(potion)
                run_data.rpgdao.use_potion(character.name, potion.id)
        else:
            print_game_delay("No items available.")
            character_battle_menu(run_data, monster)
            
# ------------------------------------------
# Levels a character's stat up when leveling
# ------------------------------------------ 
def level_character_stats(character):
    stat_options = 2
    if character.strength == 10:
        stats = ["Agility", "Intellect"]
        print(f"\nYou can improve one stat:\n"
                "1. Agility   | + Critical damage / + Dodge\n"
                "2. Intellect | + Abilities damage / - Abilities cost")
    elif character.agility == 10:
        stats = ["Strength", "Intellect"]
        print(f"\nYou can improve one stat:\n"
                "1. Strength  | + Attack / + Defense\n"
                "2. Intellect | + Abilities damage / - Abilities cost")
    elif character.intellect == 10:
        stats = ["Strength", "Agility"]
        print(f"\nYou can improve one stat:\n"
                "1. Strength  | + Attack / + Defense\n"
                "2. Agility   | + Critical damage / + Dodge\n")
    else:
        stats = ["Strength", "Agility", "Intellect"]
        print(f"\nYou can improve one stat:\n"
                "1. Strength  | + Attack / + Defense\n"
                "2. Agility   | + Critical damage / + Dodge\n"
                "3. Intellect | + Abilities damage / - Abilities cost")
        stat_options = 3
        
    op = check_option(stat_options)
    
    if op == '1':
        character.stats_up(stats[0])
        print_game_delay(f"{stats[0]} improved +1!")
    elif op == '2':
        character.stats_up(stats[1])
        print_game_delay(f"{stats[1]} improved +1!")
    elif op == '3':
        character.stats_up(stats[2])
        print_game_delay(f"{stats[2]} improved +1!")