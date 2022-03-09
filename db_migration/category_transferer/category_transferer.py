from abc import ABCMeta, abstractmethod
from db_controller.db_controller import DBController
from util.typedef import Row, Table


class CategoryTransferer(metaclass=ABCMeta):
    dbController: DBController

    categoryTransferTable: Table

    updateCategoryQuery = (
        "UPDATE posting"
        " SET category_id = %(new_category_id)s,"
        " title = CONCAT(%(old_category_name)s, title)"
        " WHERE category_id = %(old_category_id)s;")

    def __init__(self) -> None:
        self.categoryTransferTable = list()

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def transferCategory(self) -> None:
        # 1:1 transfer
        # 1:n find child
        # 1:m:n find grand child
        pass

    @abstractmethod
    def appendCategoryTransferList(self) -> None: pass

    def updateCategory(self, updateCategoryDict: Table) -> None:
        self.dbController.getCursor().executemany(
            self.updateCategoryQuery, updateCategoryDict)
        self.dbController.getDB().commit()

    def coverName(self, categoryName: str) -> str:
        return f"[{categoryName}]"
