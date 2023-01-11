import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from psycopg2 import pool

class RPGDatabase:
    
    _DATABASE = "dungeon_rpg"
    _USERNAME = "postgres"
    _PASSWORD = "admin"
    _PORT = "5432"
    _HOST = "localhost"
    _MIN_CON = 1
    _MAX_CON = 3
    
    _con_pool = None
    
    @classmethod
    def get_con_pool(cls):
        if cls._con_pool is None:
            try:
                cls._con_pool = pool.SimpleConnectionPool(cls._MIN_CON, cls._MAX_CON,
                                                         host = cls._HOST,
                                                         user = cls._USERNAME,
                                                         password = cls._PASSWORD,
                                                         port = cls._PORT,
                                                         database = cls._DATABASE)
                return cls._con_pool
            except Exception as e:
                print(f"Error ocurred while connecting database -> {e}")
                sys.exit()
        else:
            return cls._con_pool
    
    @classmethod
    def get_db_connection(cls):
        db_con = cls.get_con_pool().getconn()
        return db_con
    
    @classmethod
    def release_con(cls, con):
        cls.get_con_pool().putconn(con)
        
    @classmethod
    def close_con_pool(cls):
        cls.get_con_pool().closeall()


