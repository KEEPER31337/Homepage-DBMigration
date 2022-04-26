from abc import ABCMeta, abstractmethod
from typing import Tuple, Union
from util.typedef import IntPair, Row, Table
from util.err import RowNotFoundError
from util.db_controller import DBController
from interface.db_controllable import SingleDBControllable


class CategoryTransferer(SingleDBControllable, metaclass=ABCMeta):
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

    @abstractmethod
    def transferCategory(self) -> None: pass

    def appendCategoryTransfer(self,*args:Tuple[Union[int,IntPair]]):
        categoriesAppend = args
        for categoryAppend in categoriesAppend:
            self.appendCategoryTransferDict(categoryAppend)

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
