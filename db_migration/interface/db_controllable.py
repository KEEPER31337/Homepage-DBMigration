from abc import ABCMeta
from util.db_controller import DBController


class DBControllable(metaclass=ABCMeta):
    pass


class SingleDBControllable(DBControllable, metaclass=ABCMeta):
    _dbController: DBController

    def setDBController(self, dbController: DBController) -> None:
        self._dbController = dbController


class DoubleDBControllable(DBControllable, metaclass=ABCMeta):
    _oldDBController: DBController
    _newDBController: DBController

    def setOldDBController(self, dbController: DBController) -> None:
        self._oldDBController = dbController

    def setNewDBController(self, dbController: DBController) -> None:
        self._newDBController = dbController
