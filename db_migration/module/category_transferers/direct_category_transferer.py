from module.category_transferers.category_transferer import CategoryTransferer


class DirectCategoryTransferer(CategoryTransferer):

    # TODO 가변인자 이용
    def appendCategoryTransferDict(
            self,
            oldCategoryId: int,
            newCategoryId: int) -> None:

        categoryTransferDict = {
            "old_category_id": oldCategoryId,
            "new_category_id": newCategoryId}

        self._categoryTransferTable.append(categoryTransferDict)

    def transferCategory(self) -> None:
        self.__transferDirectCategory()

    def __transferDirectCategory(self) -> None:
        namedCategoryTransferTable = self.__getNamedTransferTable()
        self._updatePostingCategory(namedCategoryTransferTable)

    def __getNamedTransferTable(self) -> None:
        namedTransferTable = self._categoryTransferTable
        for row in namedTransferTable:
            oldCategoryName = self._getCategoryNameById(row["old_category_id"])
            row["old_category_name"] = oldCategoryName
        return namedTransferTable
