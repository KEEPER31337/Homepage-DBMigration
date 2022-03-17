from abc import ABCMeta, abstractmethod
from util.typedef import Row, Table
from util.err import RowNotFoundError
from util.db_controller import DBController


class CategoryTransferer(metaclass=ABCMeta):
    _dbController: DBController

    _categoryTransferTable: Table

    _selectCategoryNameQuery = (
        "SELECT name"
        " FROM category"
        " WHERE id = %(category_id)s;")

    _updatePostingCategoryQuery = (
        "UPDATE posting"
        " SET category_id = %(new_category_id)s,"
        " title = CONCAT(%(old_category_name)s, title)"
        " WHERE category_id = %(old_category_id)s;")

    def __init__(self) -> None:
        self._categoryTransferTable = list()

    def setDBController(self, dbController: DBController) -> None:
        self._dbController = dbController

    @abstractmethod
    def transferCategory(self) -> None: pass

    @abstractmethod
    def appendCategoryTransferDict(self) -> None: pass

    def _updatePostingCategory(self, updatePostingCategoryTable: Table) -> None:
        self._dbController.getCursor().executemany(
            self._updatePostingCategoryQuery, updatePostingCategoryTable)
        self._dbController.getDB().commit()

    def _getCategoryNameById(self, categoryId: int) -> str:
        categoryIdCol = "category_id"
        categoryIdData = {categoryIdCol: categoryId}
        selectCategoryNameCondition = f"{categoryIdCol}={categoryId}"

        categoryNameRow = self._selectCategoryName(categoryIdData)

        try:
            if not categoryNameRow:
                raise RowNotFoundError(
                    className=self.__class__.__name__,
                    methodName=self._getCategoryNameById.__name__,
                    selectCondition=selectCategoryNameCondition,
                    msg="Return empty string.")

        except RowNotFoundError as re:
            print(re)
            return ""

        categoryName = self._coverName(categoryNameRow["name"])

        return categoryName

    def _selectCategoryName(self, categoryIdData: Row) -> Row:
        cursor = self._dbController.getCursor()
        cursor.execute(self._selectCategoryNameQuery, categoryIdData)
        return cursor.fetchone()

    def _coverName(self, categoryName: str) -> str:
        return f"[{categoryName}]"
