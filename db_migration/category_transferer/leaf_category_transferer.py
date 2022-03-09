from typing import overload
from util.typedef import Row, Table
from db_controller.db_controller import DBController
from category_transferer.category_transferer import CategoryTransferer


class LeafCategoryTransfer(CategoryTransferer):
    dbController: DBController

    categoryTransferTable: Table

    leafDepth: int = 1

    updateCategoryQuery = (
        "UPDATE posting"
        " SET category_id = %(new_category_id)s,"
        " title = CONCAT(%(old_category_name)s, title)"
        " WHERE category_id = %(old_category_id)s;")

    selectChildCategoryQuery = (
        "SELECT id, parent_id, name"
        " FROM category"
        " WHERE parent_id = %(parent_category_id)s;")

    def __init__(self) -> None:
        self.categoryTransferTable = list()


    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def setLeafDepth(self, leafDepth: int) -> None:
        self.leafDepth = leafDepth

    @overload
    def appendCategoryTransferDict(self, rootCategoryId: int) -> None:
        categoryTransferDict = {
            "old_category_id": rootCategoryId,
            "new_category_id": rootCategoryId,
            "new_transferred" : False}

        self.categoryTransferTable.append(categoryTransferDict)

    @overload
    def appendCategoryTransferDict(self, rootCategoryId: int, newCategoryId: int) -> None:
        categoryTransferDict = {
            "old_category_id": rootCategoryId,
            "new_category_id": newCategoryId,
            "new_transferred" : True}

        self.categoryTransferTable.append(categoryTransferDict)

    def transferLeafCategory(self) -> None:
        unifiedLeafCategoryTable = self.getUnifiedLeafCategoryTable()

    def getUnifiedLeafCategoryTable(self) -> None:
        unifiedLeafCategoryTable: Table = list()

        for row in self.categoryTransferTable:

            childCategoryTable = self.getRootLeafChildCategory(
                row["old_category_id"])
            
            newCategoryId = row["new_category_id"]
            leafCategoryTable = self.getLeafCategoryTable(
                childCategoryTable, newCategoryId)
            unifiedLeafCategoryTable += leafCategoryTable

        return unifiedLeafCategoryTable

    def getRootLeafChildCategory(self, rootCategoryId: int):
        return self.findChildCategory(rootCategoryId, self.leafDepth)

    def findChildCategory(self, parentCategoryId: int, depth: int) -> Table:
        parentCategoryData = {"parent_category_id": parentCategoryId}

        if depth < 1:
            return list()

        childCategoryTable = self.selectChildCategory(parentCategoryData)

        if depth == 1:
            for i, row in enumerate(childCategoryTable):
                childCategoryTable[i]["name"] = self.coverName(row["name"])

            return childCategoryTable

        if depth > 1:
            unifiedChildCategoryTable = list()

            for childCategoryRow in childCategoryTable:
                categoryId = childCategoryRow["id"]
                categoryName = childCategoryRow["name"]

                grandChildCategoryTable = self.findChildCategory(
                    categoryId, depth-1)

                for i in range(len(grandChildCategoryTable)):
                    grandChildCategoryTable[i]["name"] += self.coverName(categoryName)

                unifiedChildCategoryTable += grandChildCategoryTable

        return unifiedChildCategoryTable

    def selectCategoryName(self, oldCategoryData: Row) -> Row:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectCategoryNameQuery, oldCategoryData)
        return cursor.fetchone()

    def coverName(self, categoryName: str) -> str:
        return f"[{categoryName}]"

    def getLeafCategoryTable(self, childCategoryTable: Table, newCategoryId: int):
        leafCategoryTable: Table = list()

        for childCategoryRow in childCategoryTable:
            leafCategoryDict = {
                "old_category_id": childCategoryRow["id"],
                "new_category_id": newCategoryId,
                "old_category_name": childCategoryRow["name"]}

            leafCategoryTable.append(leafCategoryDict)

        return leafCategoryTable

    def selectChildCategory(self, parentCategoryData: Row) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectChildCategoryQuery, parentCategoryData)
        return cursor.fetchall()

    def updateCategory(self) -> None:
        self.dbController.getCursor().executemany(
            self.updateCategoryQuery, self.categoryTransferTable)
        self.dbController.getDB().commit()
