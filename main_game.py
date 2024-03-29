import sys
import os

from menu.start_menu import StartMenu
from events.events import print_event, battle, loot_encounter, rest, level_character_stats

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
class_main_res = character.get_class_main_resource()
# -------------------------------------------------------------- #
#                      -> GAME STARTS <-                         #
# -------------------------------------------------------------- #

print_event("Starting game...", f"Level {run_data.floor.level} - {run_data.floor.name}", run_data.floor.description)
print("\n---------------------------------------------------------------")

while run_data.floor.level < 10:  # FLoor levels control

    event = run_data.get_random_choice("main")  # Random event probability   

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
        print_event("Going deeper into the dungeon...")
    
    character.auto_recharge_res()

    # Level ends
    if not len(run_data.floor_monsters):
        run_data.new_floor_level()
        
        if (character.level < run_data.floor.level):
            character.level_up()
            character.abilities = run_data.db_manager.rpgdao.get_character_abilities(character.character_class, run_data.floor.level)
            
            print_event(f"Level up! {character.level-1} -> {character.level}", 
                        f"HP and {character.get_class_main_resource()} restored!")
        
            level_character_stats(character)
            
        run_data.set_random_monsters()
        run_data.db_manager.rpgdao.auto_save_game(character)
        
        print_event("You have completed this level! Going to the next one...")
        
        print("\n---------------------------------------------------------------")
        
        print_event(f"Level {run_data.floor.level} - {run_data.floor.name}", 
                    run_data.floor.description)
        
        print("\n---------------------------------------------------------------")

if run_data.floor.level == 10:
    battle(run_data, run_data.db_manager.rpgdao.get_black_dragon())
    print_event(f"\n{character.name} HAS CONQUERED THE DUNGEON!")