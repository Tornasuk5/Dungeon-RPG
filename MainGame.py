import random
import time
import sys
import os

from menu.StartMenu import StartMenu
from events.Events import start_game, battle, loot_encounter, rest

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


# -------------------------------------------------------------- #
#                       -> START MENU <-                         #
# -------------------------------------------------------------- #
start_menu = StartMenu()

start_menu.load_menu()
# -------------------------------------------------------------- #
#                     -> LOAD RUN DATA <-                        #
# -------------------------------------------------------------- #
run_data = start_menu.run_data
run_data.set_random_monsters()

character = run_data.character
prob_list = run_data.prob_list
# -------------------------------------------------------------- #
#                      -> GAME STARTS <-                         #
# -------------------------------------------------------------- #

start_game(run_data.floor)

while run_data.floor.level < 10:  # FLoor levels control

    event = random.choice(run_data.prob_list)  # Random event probability

    # Chest event
    if event == "loot":
        loot_encounter(run_data)

    # Rest place event
    elif event == "rest":
        rest(character)

    # Battle event
    elif event == "battle":
        battle(run_data, run_data.get_monster())

    # Carry on
    else:
        print("\nGoing deeper into the dungeon...")

    # Level ends
    if not len(run_data.floor_monsters):
        run_data.new_floor_level()
        
        if (character.level < run_data.floor.level):
            character.level_up()
            character.abilities = run_data.db_manager.rpgdao.get_character_abilities(character.character_class, run_data.floor.level)
            
        run_data.set_random_monsters()
        run_data.db_manager.rpgdao.auto_save_game(character)
        
        print(f"\nLevel {run_data.floor.level} - {run_data.floor.name}")
        time.sleep(1)
        print(f"HP and {character.get_class_main_resource()} restored!")

    time.sleep(1)

print("\nTHE END")