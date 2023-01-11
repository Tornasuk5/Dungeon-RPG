from database.RPGDatabase import RPGDatabase

class PoolCursor:
    def __init__(self):
        self._con = None
        self._cursor = None
        
    def __enter__(self):
        self._con = RPGDatabase.get_db_connection()
        self._cursor = self._con.cursor()
        
        return self._cursor
    
    def __exit__(self, except_type, except_value, except_details):
        if except_value:
            self._con.rollback()
        else:
            self._con.commit()
            
        self._cursor.close()
        
        RPGDatabase.release_con(self._con)
        
        