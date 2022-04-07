from typing import Dict
from util.typedef import Table
from util.err import DuplicatedColumnExistErrorLog
from pymysql import OperationalError
from module.interface import SingleDBControllable, queryFormattable


class CategoryMapper(SingleDBControllable, queryFormattable):

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
            self._dbController.getCursor().execute(
                self._formatQuery(self.__addParentIdColumnFormat))
        except OperationalError as oe:
            print(DuplicatedColumnExistErrorLog(
                err=oe,
                className=self.__class__.__name__,
                methodName=self.__addParentIdColumn.__name__,
                columnName=self.__parentIdCol))

    def _formatQuery(self, queryFormat: str) -> str:
        return queryFormat.format(
            parentIdCol=self.__parentIdCol,
            newCategoryTable=self.__newCategoryTable)

    def __selectCategory(self) -> Table:
        cursor = self._dbController.getCursor()
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
        self._dbController.getCursor().executemany(
            self._formatQuery(self.__updateMappedParentIdFormat), categoryTable)
        self._dbController.getDB().commit()

    def __createNewCategoryTable(self) -> None:
        cursor = self._dbController.getCursor()
        cursor.execute(self._formatQuery(self.__createNewCategoryFormat))
        self._dbController.getDB().commit()
