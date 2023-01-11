import sys
import os
import time
from RunData import RunData
from utils.GameMethods import GameMethods

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
    
    # -------------------------
    # Prints main menu options
    # -------------------------
    def load_menu(self):
        print("Dungeon RPG - Menu\n"
              "1. New game")

        if (self.__menu_type == 1):
            print("2. Exit game")

            op = GameMethods.check_option(2)

            if op == '1':
                self.create_character()
            else:
                GameMethods.exit_game()

        else:
            print("2. Load games\n"
                  "3. Delete games\n"
                  "4. Exit game")

            op = GameMethods.check_option(4)

            if op == '1':
                self.create_character()
            elif op == '2':
                self.load_games()
            elif op == '3':
                self.delete_games()
            else:
                GameMethods.exit_game()


    # ------------------------
    # Creates a new character
    # ------------------------
    def create_character(self):
        print("Choose your class:\n"
              "1. Archer\n"
              "2. Mage\n"
              "3. Rogue\n"
              "4. Warrior")

        op = GameMethods.check_option(4, ['b'])

        if op == '1':
            character = self._run_data.db_manager.rpgdao.create_new_character("Archer")
        elif op == '2':
            character = self._run_data.db_manager.rpgdao.create_new_character("Mage")
        elif op == '3':
            character = self._run_data.db_manager.rpgdao.create_new_character("Rogue")
        elif op == '4':
            character = self._run_data.db_manager.rpgdao.create_new_character("Warrior")
        elif op == 'b':
            self.load_menu()

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
            self._run_data.set_probabilities()
        else:
            self.load_menu()  # Return to the start menu

    # ------------------
    # Loads saved games
    # ------------------
    def load_games(self):
        print("Loading saved games...")

        count = 0

        for character in self.__characters:
            count += 1
            print(f"{count}. {character.name} - Level {character.level} {character.character_class}")

        op = GameMethods.check_option(count, ['b'])

        if op == 'b':
            self.load_menu()
        else:
            character = self.__characters[int(op) - 1]
            self._main_character = character
            self._run_data.character = character
            self._run_data.set_probabilities()

    # --------------------
    # Deletes saved games
    # --------------------
    def delete_games(self):
        print("Select a game to delete it:")
        count = 0
        for character in self.__characters:
            count += 1
            print(f"{count}. {character.name} - Level {character.level} {character.character_class}")

        op = GameMethods.check_option(count, ['b'])
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
