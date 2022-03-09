from db_controller.db_controller import DBController
from util.typedef import Row, Table


class PostingCategoryTransferer:
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

    selectChildCategoryQuery = (
        "SELECT id AS old_category_id, parent_id AS new_category_id, name"
        " FROM category"
        " WHERE parent_id = %(parent_category_id)s;")

    def __init__(self) -> None:
        self.categoryTransferTable = list()

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def transferPostingCategory(self) -> None:
        # 1:1 transfer
        # 1:n find child
        # 1:m:n find grand child
        pass

    def appendCategoryTransferList(self, oldCategoryId: int, newCategoryId: int) -> None:
        oldCategoryName = self.getOldCategoryName(oldCategoryId)

        categoryTransferDict = {
            "old_category_id": oldCategoryId,
            "new_category_id": newCategoryId,
            "old_category_name" : oldCategoryName}

        self.categoryTransferTable.append(categoryTransferDict)

    def getOldCategoryName(self,oldCategoryId:int) -> str:
        oldCategoryData = {"old_category_id":oldCategoryId}
        categoryNameRow = self.selectCategoryNameQuery(oldCategoryData)
        
        oldCategoryName = categoryNameRow["name"]
        oldCategoryName = f"[{oldCategoryName}]"

        return oldCategoryName

    def selectCategoryName(self,oldCategoryData:Row) -> Row:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectCategoryNameQuery,oldCategoryData)
        return cursor.fetchone()
        

    def findChildCategory(self,parentCategoryId:int) -> Table:
        parentCategoryData = {"parent_category_id":parentCategoryId}
        childCategoryTable = self.selectChildCategory(parentCategoryData)
        self.updateCategory(childCategoryTable)

    def selectChildCategory(self,parentCategoryData:Row) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectChildCategoryQuery,parentCategoryData)
        return cursor.fetchall()

    def updateCategory(self,updateCategoryDict:Table) -> None:
        self.dbController.getCursor().executemany(
            self.updateCategoryQuery, updateCategoryDict)
        self.dbController.getDB().commit()


