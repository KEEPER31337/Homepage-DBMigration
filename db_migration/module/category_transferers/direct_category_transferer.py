from util.typedef import CategoryIdPair
from module.category_transferers.category_transferer import CategoryTransferer


class DirectCategoryTransferer(CategoryTransferer):

    def appendCategoryTransferDict(
            self,
            categoryIdPair: CategoryIdPair) -> None:

        oldCategoryId: int = categoryIdPair[0]
        newCategoryId: int = categoryIdPair[1]

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
