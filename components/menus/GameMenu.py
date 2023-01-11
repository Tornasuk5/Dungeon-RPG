import sys
from database.RPGDAO import RPGDAO
from utils.GameMethods import GameMethods

print("-----------------------\n"
      "Menu\n"
      "-----------------------\n"
      "1. Continue\n"
      "2. Open inventory\n"
      "3. Show character stats\n"
      "4. Return home\n"
      "5. Exit Game")

op = GameMethods.check_option(5)
if op == 1:
    pass
if op == 2:
    RPGDAO.open_inventory()
if op == 3:
    pass
    RPGDAO.getActualCharacter().showCharacterStats()
if op == 4:
    sys.exit("")
    import MainGame
if op == 5:
    GameMethods.exit_game()