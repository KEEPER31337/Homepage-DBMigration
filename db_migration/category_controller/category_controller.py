from typing import List, Tuple
from typedef.typedef import Table
from db_controller.db_controller import DBController


class CategoryController:
    dbController: DBController

    categoryTable: Table
    newCategoryTable: Table

    insertNewCategoryQuery = (
        "INSERT INTO category(`id`, `name`, `parent_id`, `href`"
        " VALUES(%(id)s,%(name)s,%(parent_id)s,%(href)s)")

    updateCategoryQuery = (
        "UPDATE `category`"
        " SET (`name`, `parent_id`, `href`) = (%(name)s,%(parent_id)s,%(href)s)"
        " WHERE `id` = %s")

    def __init__(self) -> None:
        self.categoryTable = list()
        self.newCategoryTable = list()

    def setDBController(self, dbController: dbController) -> None:
        self.dbController = dbController

    def appendCategoryByList(self,
                             categoryListAppend: List[Tuple[int, str, int, str]],
                             categoryTable: Table) -> None:
        for i in categoryListAppend:
            categoryTable.append(
                {"id": i[0],
                 "name": i[1],
                 "parent_id": i[2],
                 "href": i[3]})

    def insertNewCategory(self, newCategoryTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.insertNewCategoryQuery, newCategoryTable)
        self.dbController.getDB().commit()

    def updateCategory(self, categoryTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.updateCategoryQuery, categoryTable)
        self.dbController.getDB().commit()

    def controlCategory(self) -> None:
        self.insertNewCategory(self.newCategoryTable)
        self.updateCategory(self.updateCategoryQuery)
