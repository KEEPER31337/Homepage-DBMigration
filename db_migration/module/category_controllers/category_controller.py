from typing import List, Tuple
from util.typedef import Table
from interface.db_controllable import SingleDBControllable


class CategoryController(SingleDBControllable):
    __categoryTable: Table
    __newCategoryTable: Table

    # TODO : INSERT / UPDATE 통합 (ON DUPLICATE)
    __insertNewCategoryQuery = (
        "INSERT INTO category(`id`, `name`, `parent_id`, `href`)"
        " VALUES(%(id)s,%(name)s,%(parent_id)s,%(href)s);")

    __updateCategoryQuery = (
        "UPDATE `category`"
        " SET `name`=%(name)s, `parent_id`=%(parent_id)s, `href`=%(href)s"
        " WHERE `id` = %(id)s;")

    def __init__(self) -> None:
        self.__categoryTable = list()
        self.__newCategoryTable = list()

    def appendCategoryByList(self,
                             categoryListAppend: List[Tuple[int, str, int, str]],
                             categoryTable: Table) -> None:
        for i in categoryListAppend:
            categoryTable.append(
                {"id": i[0],
                 "name": i[1],
                 "parent_id": i[2],
                 "href": i[3]})

    def controlCategory(self) -> None:
        self.__insertNewCategory(self.__newCategoryTable)
        self.__updateCategory(self.__categoryTable)

    def __insertNewCategory(self, newCategoryTable: Table) -> None:
        self._dbController.getCursor().executemany(
            self.__insertNewCategoryQuery, newCategoryTable)
        self._dbController.getDB().commit()

    def __updateCategory(self, categoryTable: Table) -> None:
        self._dbController.getCursor().executemany(
            self.__updateCategoryQuery, categoryTable)
        self._dbController.getDB().commit()
