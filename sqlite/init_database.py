import sqlite3

try:
    print("Generating dungeon... ⌛")
    dungeon_db = sqlite3.connect("sqlite/database/dungeon_rpg.db")
    cursor = dungeon_db.cursor()
    
    with open('sqlite/database/dungeon_rpg_data.sql', 'r') as data_script:
        dungeon_data = data_script.read() 

    cursor.executescript(dungeon_data)
    
    dungeon_db.commit()
    dungeon_db.close()
    
except Exception as x:
    print(x)

        


