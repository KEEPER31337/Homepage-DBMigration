from category_transferers.category_transferer import CategoryTransferer


class DirectCategoryTransferer(CategoryTransferer):

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
            oldCategoryName = self.getCategoryNameById(row["old_category_id"])
            row["old_category_name"] = oldCategoryName
        return namedTransferTable
