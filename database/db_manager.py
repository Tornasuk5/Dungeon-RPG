from database.rpgdao import RPGDAO

class DBManager:
    def __init__(self):
        self._rpgdao = RPGDAO
    
    @property
    def rpgdao(self):
        return self._rpgdao