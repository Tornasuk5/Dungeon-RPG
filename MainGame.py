import random
import time
import sys
import os

from StartMenu import StartMenu
from events.Events import Events

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)


# -------------------------------------------------------------- #
#                       -> START MENU <-                         #
# -------------------------------------------------------------- #
start_menu = StartMenu()

start_menu.load_menu()

run_data = start_menu.run_data
run_data.set_random_monsters()

prob_list = run_data.prob_list

Events.start_game(run_data.floor)

while run_data.floor.level < 10:  # FLoor levels control

    event = random.choice(run_data.prob_list)  # Random event probability

    # Chest event
    if event == "loot":
        Events.loot_encounter(run_data)

    # Rest place event
    elif event == "rest":
        Events.rest(run_data.character)

    # Battle event
    elif event == "battle":
        Events.battle(run_data, run_data.get_monster())

    # Carry on
    else:
        print("Going deeper into the dungeon...")

    # Level end
    if not len(run_data.floor_monsters):
        run_data.new_floor_level()
        run_data.character.level_up()
        run_data.character.set_new_abilities(run_data.db_manager.rpgdao
                                             .get_character_abilities(run_data.character.character_class, run_data.floor.level))
        run_data.set_random_monsters()
        
        print(f"Level {run_data.floor.level} - {run_data.floor.name}\n")

    time.sleep(1)

    print("")

else:
    print("THE END")
