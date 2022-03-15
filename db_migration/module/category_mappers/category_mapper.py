from typing import Dict
from util.err import DuplicatedColumnExistErrorLog
from util.typedef import Table
from pymysql import OperationalError
from util.db_controller import DBController


class CategoryMapper:

    dbController: DBController
    parentIdCol: str
    newCategoryTable: str

    selectCategoryQuery = (
        "SELECT t1.module_srl, t2.menu_item_srl, t2.parent_srl"
        " FROM xe_modules AS t1 JOIN xe_menu_item AS t2"
        " ON t1.mid = t2.url;")

    addParentIdColumnFormat = (
        "ALTER TABLE xe_modules"
        " ADD {parentIdCol} INT DEFAULT NULL")

    updateMappedParentIdFormat = (
        "UPDATE xe_modules"
        " SET {parentIdCol} = %({parentIdCol})s"
        " WHERE module_srl = %(module_srl)s;")

    createNewCategoryFormat = (
        "DROP TABLE IF EXISTS {newCategoryTable};"
        "CREATE TABLE {newCategoryTable} ("
        "SELECT t1.module_srl, t2.name, t1.{parentIdCol}"
        " FROM xe_modules AS t1 JOIN xe_menu_item AS t2"
        " ON t1.mid = t2.url);")

    def __init__(self,
                 parentIdCol: str = "module_parent_srl",
                 newCategoryTable: str = "new_category") -> None:
        self.parentIdCol = parentIdCol
        self.newCategoryTable = newCategoryTable

    def formatAddParentIdColumnQuery(self) -> str:
        return self.addParentIdColumnFormat.format(parentIdCol=self.parentIdCol)

    def formatUpdateMappedParentIdQuery(self) -> str:
        return self.updateMappedParentIdFormat.format(parentIdCol=self.parentIdCol)

    def formatCreateNewCategoryQuery(self) -> str:
        return self.createNewCategoryFormat.format(
            parentIdCol=self.parentIdCol,
            newCategoryTable=self.newCategoryTable)

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def mapCategory(self) -> None:
        self.addParentIdColumn()

        categoryTable = self.selectCategory()
        categoryTable = self.mapModuleMenuItemSrl(
            categoryTable, self.getModuleMenuItemSrlDict(categoryTable))
        self.updateCategoryTable(categoryTable)

        self.createNewCategoryTable()

    def addParentIdColumn(self) -> None:
        try:
            self.dbController.getCursor().execute(self.formatAddParentIdColumnQuery())
        except OperationalError as oe:
            print(DuplicatedColumnExistErrorLog(
                err=oe,
                className=self.__class__.__name__,
                methodName=self.addParentIdColumn.__name__,
                columnName=self.parentIdCol))

    def selectCategory(self) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectCategoryQuery)
        tableContent = cursor.fetchall()
        return tableContent

    def mapModuleMenuItemSrl(self, moduleMenuItemSrlTable: Table,
                             moduleMenuItemSrlDict: Dict[int, int]) -> Table:

        for row in moduleMenuItemSrlTable:
            row[self.parentIdCol] = moduleMenuItemSrlDict[row["parent_srl"]]

        return moduleMenuItemSrlTable

    def getModuleMenuItemSrlDict(self, moduleMenuItemSrlTable: Table) -> Dict[int, int]:
        moduleMenuItemSrlDict = self.addRootCategoryDict()

        for row in moduleMenuItemSrlTable:
            moduleMenuItemSrlDict[
                row["menu_item_srl"]] = row["module_srl"]

        return moduleMenuItemSrlDict

    def addRootCategoryDict(self) -> Dict[int, int]:
        moduleMenuItemSrlDict: Dict[int, int] = {0: 0}
        return moduleMenuItemSrlDict

    def updateCategoryTable(self, categoryTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.formatUpdateMappedParentIdQuery(), categoryTable)
        self.dbController.getDB().commit()

    def createNewCategoryTable(self) -> None:
        cursor = self.dbController.getCursor()
        cursor.execute(self.formatCreateNewCategoryQuery())
        self.dbController.getDB().commit()
