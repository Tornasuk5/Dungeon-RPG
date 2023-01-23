import sys
import time

#-------------------------------------------
# Validates the option choosen by the player
#-------------------------------------------
@staticmethod
def check_option(num_ops, extra_ops = []):
    op = 0;
    valid_option = False
    
    while not valid_option:
        try:
            op = input("-> ")
            
            if int(op) <= 0 or int(op) > num_ops: 
                print("Comando incorrecto, vuelva a intentarlo")
            else: 
                valid_option = True
            
        except:
            if len(extra_ops) > 0:
                
                if op == 'b':
                    valid_option = True
                else: 
                    print("Comando incorrecto, vuelva a intentarlo")
                    
            else: 
                print("Comando incorrecto, vuelva a intentarlo")
            
    return op

#----------------------
# Prints a line of text
#----------------------
@staticmethod
def print_game_delay(text):
    print(f"\n{text}")
    time.sleep(1)

#----------------
# Closes the game
#----------------
@staticmethod
def exit_game():
    sys.exit("Game closed.")

'''
#--------------------------
# Shows game's menu options
#--------------------------
@classmethod
def show_menu(cls, run_data):
    print("-----------------------\n"
    "Menu\n"
    "-----------------------\n"
    "1. Continue\n"
    "2. Open inventory\n"
    "3. Show character stats\n"
    "4. Return home\n"
    "5. Exit Game")

    op = cls.check_option(5)
    if op == 1:
        pass
    if op == 2:
        run_data.rpgdao.open_inventory()
    if op == 3:
        pass
        run_data.character.show_character_stats()
    if op == 4:
        sys.exit("")
        import main_game
    if op == 5:
        cls.exit_game()
'''