from abc import ABCMeta, abstractmethod
from util.typedef import Row, Table
from util.err import RowNotFoundError
from db_controller.db_controller import DBController


class CategoryTransferer(metaclass=ABCMeta):
    dbController: DBController

    categoryTransferTable: Table

    selectCategoryNameQuery = (
        "SELECT name"
        " FROM category"
        " WHERE id = %(category_id)s;")

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
    def appendCategoryTransferDict(self) -> None: pass

    def updatePostingCategory(self, updatePostingCategoryTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.updatePostingCategoryQuery, updatePostingCategoryTable)
        self.dbController.getDB().commit()

    def getCategoryNameById(self, categoryId: int) -> str:
        categoryIdCol = "category_id"
        categoryIdData = {categoryIdCol: categoryId}
        selectCategoryNameCondition = f"{categoryIdCol}={categoryId}"

        categoryNameRow = self.selectCategoryName(categoryIdData)

        try:
            if not categoryNameRow:
                raise RowNotFoundError(
                    className=self.__class__.__name__,
                    methodName=self.getCategoryNameById.__name__,
                    selectCondition=selectCategoryNameCondition,
                    msg="Return empty string.")

        except RowNotFoundError as re:
            print(re)
            return ""

        categoryName = self.coverName(categoryNameRow["name"])

        return categoryName

    def selectCategoryName(self, categoryIdData: Row) -> Row:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectCategoryNameQuery, categoryIdData)
        return cursor.fetchone()

    def coverName(self, categoryName: str) -> str:
        return f"[{categoryName}]"
