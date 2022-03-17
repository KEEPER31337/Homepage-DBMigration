from typing import List, Tuple
from util.typedef import Table
from util.db_controller import DBController


class CategoryController:
    __dbController: DBController

    __categoryTable: Table
    __newCategoryTable: Table

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

    def setDBController(self, dbController: DBController) -> None:
        self.__dbController = dbController

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
        self.__dbController.getCursor().executemany(
            self.__insertNewCategoryQuery, newCategoryTable)
        self.__dbController.getDB().commit()

    def __updateCategory(self, categoryTable: Table) -> None:
        self.__dbController.getCursor().executemany(
            self.__updateCategoryQuery, categoryTable)
        self.__dbController.getDB().commit()
