from util.typedef import Row
from category_transferer.category_transferer import CategoryTransferer


class DirectCategoryTransferer(CategoryTransferer):

    selectCategoryNameQuery = (
        "SELECT name"
        " FROM category"
        " WHERE id = %(old_category_id)s;")

    def appendCategoryTransferDict(self, oldCategoryId: int, newCategoryId: int) -> None:
        categoryTransferDict = {
            "old_category_id": oldCategoryId,
            "new_category_id": newCategoryId}

        self.categoryTransferTable.append(categoryTransferDict)

    def transferCategory(self) -> None:
        self.transferDirectCategory()

    def transferDirectCategory(self) -> None:
        namedCategoryTransferTable = self.getNamedTransferTable()
        self.updatePostingCategory(namedCategoryTransferTable)

    def getNamedTransferTable(self) -> None:
        namedTransferTable = self.categoryTransferTable

        for row in namedTransferTable:
            oldCategoryName = self.getOldCategoryName(row["old_category_id"])
            namedTransferTable["old_category_name"] = oldCategoryName

        return namedTransferTable

    def getOldCategoryName(self, oldCategoryId: int) -> str:
        oldCategoryData = {"old_category_id": oldCategoryId}
        categoryNameRow = self.selectCategoryNameQuery(oldCategoryData)

        oldCategoryName = self.coverName(categoryNameRow["name"])

        return oldCategoryName

    def selectCategoryName(self, oldCategoryData: Row) -> Row:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectCategoryNameQuery, oldCategoryData)
        return cursor.fetchone()
