from category_transferer.category_transferer import CategoryTransferer
from db_controller.db_controller import DBController
from util.typedef import Row, Table


class DirectCategoryTransferer(CategoryTransferer):
    dbController: DBController

    categoryTransferTable: Table

    selectCategoryNameQuery = (
        "SELECT name"
        " FROM category"
        " WHERE id = %(old_category_id)s;")

    updateCategoryQuery = (
        "UPDATE posting"
        " SET category_id = %(new_category_id)s,"
        " title = CONCAT(%(old_category_name)s, title)"
        " WHERE category_id = %(old_category_id)s;")

    def __init__(self) -> None:
        self.categoryTransferTable = list()

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def appendCategoryTransferDict(self, oldCategoryId: int, newCategoryId: int) -> None:
        categoryTransferDict = {
            "old_category_id": oldCategoryId,
            "new_category_id": newCategoryId}

        self.categoryTransferTable.append(categoryTransferDict)

    def transferDirectCategory(self) -> None:
        namedCategoryTransferTable = self.getNamedTransferTable()
        self.updateCategory(namedCategoryTransferTable)

    def getNamedTransferTable(self) -> None:
        namedTransferTable = self.categoryTransferTable

        for row in namedTransferTable:
            oldCategoryName = self.getOldCategoryName(row["old_category_id"])
            namedTransferTable["old_category_name"] = oldCategoryName

        return namedTransferTable

    def getOldCategoryName(self, oldCategoryId: int) -> str:
        oldCategoryData = {"old_category_id": oldCategoryId}
        categoryNameRow = self.selectCategoryNameQuery(oldCategoryData)

        oldCategoryName = categoryNameRow["name"]
        oldCategoryName = f"[{oldCategoryName}]"

        return oldCategoryName

    def selectCategoryName(self, oldCategoryData: Row) -> Row:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectCategoryNameQuery, oldCategoryData)
        return cursor.fetchone()

    def updateCategory(self, categoryTransferTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.updateCategoryQuery, categoryTransferTable)
        self.dbController.getDB().commit()
