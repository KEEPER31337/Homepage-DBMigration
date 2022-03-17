from typing import Dict
from util.err import DuplicatedColumnExistErrorLog
from util.typedef import Table
from pymysql import OperationalError
from util.db_controller import DBController


class CategoryMapper:

    __dbController: DBController
    __parentIdCol: str
    __newCategoryTable: str

    __selectCategoryQuery = (
        "SELECT t1.module_srl, t2.menu_item_srl, t2.parent_srl"
        " FROM xe_modules AS t1 JOIN xe_menu_item AS t2"
        " ON t1.mid = t2.url;")

    __addParentIdColumnFormat = (
        "ALTER TABLE xe_modules"
        " ADD {parentIdCol} INT DEFAULT NULL")

    __updateMappedParentIdFormat = (
        "UPDATE xe_modules"
        " SET {parentIdCol} = %({parentIdCol})s"
        " WHERE module_srl = %(module_srl)s;")

    __createNewCategoryFormat = (
        "DROP TABLE IF EXISTS {newCategoryTable};"
        "CREATE TABLE {newCategoryTable} ("
        "SELECT t1.module_srl, t2.name, t1.{parentIdCol}"
        " FROM xe_modules AS t1 JOIN xe_menu_item AS t2"
        " ON t1.mid = t2.url);")

    def __init__(self,
                 parentIdCol: str = "module_parent_srl",
                 newCategoryTable: str = "new_category") -> None:
        self.__parentIdCol = parentIdCol
        self.__newCategoryTable = newCategoryTable

    def setDBController(self, dbController: DBController) -> None:
        self.__dbController = dbController

    def mapCategory(self) -> None:
        self.__addParentIdColumn()

        categoryTable = self.__selectCategory()

        moduleMenuItemSrlDict = self.__getModuleMenuItemSrlDict(categoryTable)

        categoryTable = self.__mapModuleMenuItemSrl(
            categoryTable, moduleMenuItemSrlDict)
        self.__updateCategoryTable(categoryTable)

        self.__createNewCategoryTable()

    def __addParentIdColumn(self) -> None:
        try:
            self.__dbController.getCursor().execute(self.__formatAddParentIdColumnQuery())
        except OperationalError as oe:
            print(DuplicatedColumnExistErrorLog(
                err=oe,
                className=self.__class__.__name__,
                methodName=self.__addParentIdColumn.__name__,
                columnName=self.__parentIdCol))

    def __formatAddParentIdColumnQuery(self) -> str:
        return self.__addParentIdColumnFormat.format(parentIdCol=self.__parentIdCol)

    def __selectCategory(self) -> Table:
        cursor = self.__dbController.getCursor()
        cursor.execute(self.__selectCategoryQuery)
        tableContent = cursor.fetchall()
        return tableContent

    def __mapModuleMenuItemSrl(self, moduleMenuItemSrlTable: Table,
                               moduleMenuItemSrlDict: Dict[int, int]) -> Table:

        for row in moduleMenuItemSrlTable:
            row[self.__parentIdCol] = moduleMenuItemSrlDict[row["parent_srl"]]

        return moduleMenuItemSrlTable

    def __getModuleMenuItemSrlDict(self, moduleMenuItemSrlTable: Table) -> Dict[int, int]:
        moduleMenuItemSrlDict = self.__addRootCategoryDict()

        for row in moduleMenuItemSrlTable:
            moduleMenuItemSrlDict[
                row["menu_item_srl"]] = row["module_srl"]

        return moduleMenuItemSrlDict

    def __addRootCategoryDict(self) -> Dict[int, int]:
        moduleMenuItemSrlDict: Dict[int, int] = {0: 0}
        return moduleMenuItemSrlDict

    def __updateCategoryTable(self, categoryTable: Table) -> None:
        self.__dbController.getCursor().executemany(
            self.__formatUpdateMappedParentIdQuery(), categoryTable)
        self.__dbController.getDB().commit()

    def __formatUpdateMappedParentIdQuery(self) -> str:
        return self.__updateMappedParentIdFormat.format(parentIdCol=self.__parentIdCol)

    def __createNewCategoryTable(self) -> None:
        cursor = self.__dbController.getCursor()
        cursor.execute(self.__formatCreateNewCategoryQuery())
        self.__dbController.getDB().commit()

    def __formatCreateNewCategoryQuery(self) -> str:
        return self.__createNewCategoryFormat.format(
            parentIdCol=self.__parentIdCol,
            newCategoryTable=self.__newCategoryTable)
