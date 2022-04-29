from typing import Tuple
from util.typedef import CategoryInfo, Table
from interface.db_controllable import SingleDBControllable


class CategoryController(SingleDBControllable):
    __categoryTable: Table

    __insertCategoryQuery = (
        "INSERT INTO category(id, name, parent_id, href)"
        " VALUES(%(id)s,%(name)s,%(parent_id)s,%(href)s)"
        " ON DUPLICATE KEY"
        " UPDATE name=%(name)s, parent_id=%(parent_id)s, href=%(href)s;")

    def __init__(self) -> None:
        self.__categoryTable = list()

    def appendCategory(
            self,
            *categoriesAppend: Tuple[CategoryInfo]) -> None:

        for categoryAppend in categoriesAppend:
            self.__categoryTable.append(
                {"id": categoryAppend[0],
                 "name": categoryAppend[1],
                 "parent_id": categoryAppend[2],
                 "href": categoryAppend[3]})

    def controlCategory(self) -> None:
        self.__insertCategory(self.__categoryTable)

    def __insertCategory(self, categoryTable: Table) -> None:
        self._dbController.getCursor().executemany(
            self.__insertCategoryQuery, categoryTable)
        self._dbController.getDB().commit()
