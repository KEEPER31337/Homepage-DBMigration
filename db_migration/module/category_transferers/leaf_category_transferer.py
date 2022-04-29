from multipledispatch import dispatch
from util.typedef import CategoryIdPair, Row, Table
from module.category_transferers.category_transferer import CategoryTransferer


class LeafCategoryTransferer(CategoryTransferer):

    __leafDepth: int = 1

    __selectChildCategoryQuery = (
        "SELECT id, parent_id, name"
        " FROM category"
        " WHERE parent_id = %(parent_category_id)s;")

    def setLeafDepth(self, leafDepth: int) -> None:
        self.__leafDepth = leafDepth

    @dispatch(int)
    def appendCategoryTransferDict(
            self,
            rootCategoryId: int) -> None:

        categoryTransferDict = {
            "old_category_id": rootCategoryId,
            "new_category_id": rootCategoryId,
            "new_transferred": False}

        self._categoryTransferTable.append(categoryTransferDict)

    @dispatch(tuple)
    def appendCategoryTransferDict(
            self,
            categoryIdPair: CategoryIdPair) -> None:

        rootCategoryId: int = categoryIdPair[0]
        newCategoryId: int = categoryIdPair[1]

        categoryTransferDict = {
            "old_category_id": rootCategoryId,
            "new_category_id": newCategoryId,
            "new_transferred": True}

        self._categoryTransferTable.append(categoryTransferDict)

    def transferCategory(self) -> None:
        self.__transferLeafCategory()

    def __transferLeafCategory(self) -> None:
        unifiedLeafCategoryTable = self.__getUnifiedLeafCategoryTable()
        self._updatePostingCategory(unifiedLeafCategoryTable)

    def __getUnifiedLeafCategoryTable(self) -> None:
        unifiedLeafCategoryTable: Table = list()

        for row in self._categoryTransferTable:

            leafChildCategoryTable = self.__getRootLeafChildCategory(row)

            newCategoryId = row["new_category_id"]
            leafCategoryTable = self.__getLeafCategoryTable(
                leafChildCategoryTable, newCategoryId)
            unifiedLeafCategoryTable += leafCategoryTable

        return unifiedLeafCategoryTable

    def __getRootLeafChildCategory(self, categoryTransfer: Row) -> Table:
        rootCategoryId = categoryTransfer["old_category_id"]
        newTransferred = categoryTransfer["new_transferred"]

        leafChildCategoryTable = self.__findChildCategory(
            rootCategoryId, self.__leafDepth)

        if newTransferred:
            rootCategoryName = self._getCategoryNameById(rootCategoryId)

            for i, row in enumerate(leafChildCategoryTable):
                leafChildCategoryTable[i]["name"] = f"{rootCategoryName}{row['name']}"

        return leafChildCategoryTable

    def __findChildCategory(self, parentCategoryId: int, depth: int) -> Table:
        parentCategoryData = {"parent_category_id": parentCategoryId}

        if depth < 1:
            return list()

        childCategoryTable = self.__selectChildCategory(parentCategoryData)

        if depth == 1:
            for i, row in enumerate(childCategoryTable):
                childCategoryTable[i]["name"] = self._coverName(row["name"])

            return childCategoryTable

        if depth > 1:
            leafChildCategoryTable = list()

            for childCategoryRow in childCategoryTable:
                categoryId = childCategoryRow["id"]
                categoryName = childCategoryRow["name"]

                grandChildCategoryTable = self.__findChildCategory(
                    categoryId, depth-1)

                for i, row in enumerate(grandChildCategoryTable):
                    grandChildCategoryTable[i]["name"] = f"{self._coverName(categoryName)}{row['name']}"

                leafChildCategoryTable += grandChildCategoryTable

        return leafChildCategoryTable

    def __selectChildCategory(self, parentCategoryData: Row) -> Table:
        cursor = self._dbController.getCursor()
        cursor.execute(self.__selectChildCategoryQuery, parentCategoryData)
        return cursor.fetchall()

    def __getLeafCategoryTable(self, childCategoryTable: Table, newCategoryId: int) -> Table:
        leafCategoryTable: Table = list()

        for childCategoryRow in childCategoryTable:
            leafCategoryDict = {
                "old_category_id": childCategoryRow["id"],
                "new_category_id": newCategoryId,
                "old_category_name": childCategoryRow["name"]}

            leafCategoryTable.append(leafCategoryDict)

        return leafCategoryTable
