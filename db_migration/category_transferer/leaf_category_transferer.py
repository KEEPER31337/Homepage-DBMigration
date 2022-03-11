from util.typedef import Row, Table
from category_transferer.category_transferer import CategoryTransferer


class LeafCategoryTransferer(CategoryTransferer):

    leafDepth: int = 1

    selectChildCategoryQuery = (
        "SELECT id, parent_id, name"
        " FROM category"
        " WHERE parent_id = %(parent_category_id)s;")

    def setLeafDepth(self, leafDepth: int) -> None:
        self.leafDepth = leafDepth

    # simillar overloading
    def appendCategoryTransferDict(self, rootCategoryId: int, newCategoryId: int = None) -> None:

        isNewTransferred = not newCategoryId
        if isNewTransferred:
            newCategoryId = rootCategoryId

        categoryTransferDict = {
            "old_category_id": rootCategoryId,
            "new_category_id": newCategoryId,
            "new_transferred": isNewTransferred}

        self.categoryTransferTable.append(categoryTransferDict)

    def transferCategory(self) -> None:
        self.transferLeafCategory()

    def transferLeafCategory(self) -> None:
        unifiedLeafCategoryTable = self.getUnifiedLeafCategoryTable()
        self.updatePostingCategory(unifiedLeafCategoryTable)

    def getUnifiedLeafCategoryTable(self) -> None:
        unifiedLeafCategoryTable: Table = list()

        for row in self.categoryTransferTable:

            leafChildCategoryTable = self.getRootLeafChildCategory(row)

            newCategoryId = row["new_category_id"]
            leafCategoryTable = self.getLeafCategoryTable(
                leafChildCategoryTable, newCategoryId)
            unifiedLeafCategoryTable += leafCategoryTable

        return unifiedLeafCategoryTable

    def getRootLeafChildCategory(self, categoryTransfer: Row) -> Table:
        rootCategoryId = categoryTransfer["old_category_id"]
        newTransferred = categoryTransfer["new_transferred"]
        
        leafChildCategoryTable = self.findChildCategory(
            rootCategoryId, self.leafDepth)

        if newTransferred:
            rootCategoryName = self.getCategoryNameById(rootCategoryId)

            for i, row in enumerate(leafChildCategoryTable):
                leafChildCategoryTable[i]["name"] = f"{self.coverName(rootCategoryName)}{row['name']}"

        return leafChildCategoryTable

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
            leafChildCategoryTable = list()

            for childCategoryRow in childCategoryTable:
                categoryId = childCategoryRow["id"]
                categoryName = childCategoryRow["name"]

                grandChildCategoryTable = self.findChildCategory(
                    categoryId, depth-1)

                for i, row in enumerate(grandChildCategoryTable):
                    grandChildCategoryTable[i]["name"] = f"{self.coverName(categoryName)}{row['name']}"

                leafChildCategoryTable += grandChildCategoryTable

        return leafChildCategoryTable

    def selectChildCategory(self, parentCategoryData: Row) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectChildCategoryQuery, parentCategoryData)
        return cursor.fetchall()

    def getLeafCategoryTable(self, childCategoryTable: Table, newCategoryId: int) -> Table:
        leafCategoryTable: Table = list()

        for childCategoryRow in childCategoryTable:
            leafCategoryDict = {
                "old_category_id": childCategoryRow["id"],
                "new_category_id": newCategoryId,
                "old_category_name": childCategoryRow["name"]}

            leafCategoryTable.append(leafCategoryDict)

        return leafCategoryTable
