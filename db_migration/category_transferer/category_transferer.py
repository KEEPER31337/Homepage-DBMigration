from abc import ABCMeta, abstractmethod
from db_controller.db_controller import DBController
from util.typedef import Table


class CategoryTransferer(metaclass=ABCMeta):
    dbController: DBController

    categoryTransferTable: Table

    updatePostingCategoryQuery = (
        "UPDATE posting"
        " SET category_id = %(new_category_id)s,"
        " title = CONCAT(%(old_category_name)s, title)"
        " WHERE category_id = %(old_category_id)s;")

    def __init__(self) -> None:
        self.categoryTransferTable = list()

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    @abstractmethod
    def transferCategory(self) -> None: pass

    @abstractmethod
    def appendCategoryTransferList(self) -> None: pass

    def updatePostingCategory(self, updatePostingCategoryTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.updatePostingCategoryQuery, updatePostingCategoryTable)
        self.dbController.getDB().commit()

    def coverName(self, categoryName: str) -> str:
        return f"[{categoryName}]"
