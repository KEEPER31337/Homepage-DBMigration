from abc import ABCMeta, abstractmethod
from util.db_controller import DBController


class FormatInterface(metaclass=ABCMeta):

    @abstractmethod
    def _formatQuery(self) -> None:
        pass


class DBControllInterface(metaclass=ABCMeta):
    _dbController: DBController

    def setDBController(self, dbController: DBController) -> None:
        self._dbController = dbController


class DoubleDBControllInterface(metaclass=ABCMeta):
    _oldDBController: DBController
    _newDBController: DBController

    def setOldDBController(self, dbController: DBController) -> None:
        self._oldDBController = dbController

    def setNewDBController(self, dbController: DBController) -> None:
        self._newDBController = dbController
