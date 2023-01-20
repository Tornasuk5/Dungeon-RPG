import sys
import os
import time
from rundata.run_data import RunData
from utils.game_methods import check_option, exit_game

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

class StartMenu:
    def __init__(self):
        self._run_data = RunData()
        
        self.__characters = self._run_data.db_manager.rpgdao.get_characters()

        self._main_character = ""

        if len(self.__characters) == 0:
            self.__menu_type = 1 # There are no character in db -> Menu shows only 'New game' and 'Exit game' options
        else:
            self.__menu_type = 2 # There are characters in db -> Menu shows 'Load games' and 'Delete games' options besides of 'New game' and 'Exit game'
    
    @property
    def main_character(self):
        return self._main_character
    
    @property
    def run_data(self):
        return self._run_data
    
    # ----------------------------
    # Prints the main menu options
    # ----------------------------
    def load_menu(self):
        print("\nDungeon RPG - Menu\n"
              "1. New game")

        if (self.__menu_type == 1):
            print("2. Exit game")

            op = check_option(2)

            if op == '1':
                self.create_character()
            else:
                exit_game()

        else:
            print("2. Load games\n"
                  "3. Delete games\n"
                  "4. Exit game")

            op = check_option(4)

            if op == '1':
                self.create_character()
            elif op == '2':
                self.load_run()
            elif op == '3':
                self.delete_game()
            else:
                exit_game()


    # -----------------------
    # Creates a new character
    # -----------------------
    def create_character(self):
        print("\nChoose your class:\n"
              "1. Hunter\n"
              "2. Mage\n"
              "3. Rogue\n"
              "4. Warrior")

        op = check_option(4, ['b'])

        if op == '1':
            character = self._run_data.db_manager.rpgdao.create_new_character("Hunter")
        elif op == '2':
            character = self._run_data.db_manager.rpgdao.create_new_character("Mage")
        elif op == '3':
            character = self._run_data.db_manager.rpgdao.create_new_character("Rogue")
        elif op == '4':
            character = self._run_data.db_manager.rpgdao.create_new_character("Warrior")
            
        if op == 'b':
            self.load_menu()
        else:
            name = ""
            check_name = False

            while not check_name:
                name = input("Character's name: ")
                if self._run_data.db_manager.rpgdao.check_new_character_name(name):
                    print("Character's name already exist, try other")
                else:
                    check_name = True

            character.name = name
            character.show_character_stats()

            start = input("Enter into The Dungeon? (Y / N) -> ")

            if start.lower() == 'y':
                self._run_data.db_manager.rpgdao.save_character(character)  # Save new character in db
                
                self._main_character = character  # Save new character's name in order to get it in the main game script
                self._run_data.character = character
            else:
                self.load_menu()  # Return to the start menu

    # ----------------
    # Loads saved runs
    # ----------------
    def load_run(self):
        print("\nLoading saved games...")

        count = 0

        for character in self.__characters:
            count += 1
            print(f"{count}. {character.name} - Level {character.level} {character.character_class}")

        op = check_option(count, ['b'])

        if op == 'b':
            self.load_menu()
        else:
            character = self.__characters[int(op) - 1]
            character.abilities = self._run_data.db_manager.rpgdao.get_character_abilities(character.character_class, character.level)
            self._main_character = character
            self._run_data.character = character

    #--------------------
    # Deletes a character
    #--------------------
    def delete_game(self):
        print("\nSelect a game:")
        count = 0
        for character in self.__characters:
            count += 1
            print(f"{count}. {character.name} - Level {character.level} {character.character_class}")

        op = check_option(count, ['b'])
        if op == 'b':
            self.load_menu()
        else:
            self._run_data.db_manager.rpgdao.delete_game(self.__characters.pop(int(op)-1).name)
            time.sleep(1)

            if len(self.__characters) >= 1:
                self.load_menu()
            else:
                self.__menu_type = 1
                self.load_menu()
