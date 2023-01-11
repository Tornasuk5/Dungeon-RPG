from database.RPGDAO import RPGDAO

class DBManager:
    def __init__(self):
        self._rpgdao = RPGDAO
    
    @property
    def rpgdao(self):
        return self._rpgdao