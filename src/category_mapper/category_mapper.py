from typing import Dict
from db_controller.db_controller import DBController
from pymysql import OperationalError
from typedef.typedef import Row, Table


class CategoryMapper:
    
    dbController: DBController

    selectCategoryQuery = (
        "SELECT t1.module_srl, t2.menu_item_srl, t2.parent_srl"
        " FROM xe_modules AS t1 JOIN xe_menu_item AS t2"
        " ON t1.mid = t2.url;")

    addParentIdColumnQuery = (
        "ALTER TABLE xe_modules"
        " ADD parent_id INT DEFAULT NULL")

    updateMappedParentIdQuery = (
        "UPDATE xe_modules"
        " SET parent_id = %(parent_id)s"
        " WHERE module_srl = %(module_srl)s;"
    )

    def __init__(self) -> None:
        pass

    def setDBController(self,dbController: DBController) -> None:
        self.dbController = dbController

    def addParentIdColumn(self) -> None:
        try:
            self.dbController.getCursor().execute(self.addParentIdColumnQuery)
        except OperationalError as oe:
            print(f"{oe} : There is a column already. From {self.addParentIdColumn.__name__}.")

    def selectCategory(self) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectCategoryQuery)
        tableContent = cursor.fetchall()
        return tableContent

    def getModuleMenuItemSrlDict(self,moduleMenuItemSrlTable: Table):
        moduleMenuItemSrlDict = dict()

        for row in moduleMenuItemSrlTable:
            moduleMenuItemSrlDict[
                row["menu_item_srl"]] = row["module_srl"]

        return moduleMenuItemSrlDict


    def mapModuleMenuItemSrl(self, moduleMenuItemSrlTable: Table, moduleMenuItemSrlDict: Dict) :

        for row in moduleMenuItemSrlTable:
            row["parent_id"] = moduleMenuItemSrlDict[row["parent_srl"]]

        return moduleMenuItemSrlTable

    def updateCategoryTable(self, categoryTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.updateMappedParentIdQuery, categoryTable)
        self.dbController.getDB().commit()


    def mapCategory(self) -> None:
        self.addParentIdColumn()
        categoryTable = self.selectCategory()
        categoryTable = self.mapModuleMenuItemSrl(categoryTable, self.getModuleMenuItemSrlDict(categoryTable))
        self.updateCategoryTable(categoryTable)

    
