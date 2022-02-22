from db_controller.db_controller import DBController
from typedef.typedef import Table


class ParentPuller:
    dbController: DBController

    tableReset: Table

    selectCommentQuery = (
        "SELECT comment_srl, parent_srl"
        " FROM xe_comments;")

    updateCommentQuery = (
        "UPDATE xe_comments"
        " SET parent_srl=%(parent_srl)s"
        " WHERE comment_srl=%(comments_srl)s;")

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def selectComment(self) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectCommentQuery)
        return cursor.fetchall()

    def initVisited(self):
        for i in range(len(self.tableReset)):
            self.tableReset[i]["visited"] = False

    def pullUpParentSrl(self) -> Table:
        for i, row in enumerate(self.tableReset):
            rowParentSrl = row["parent_srl"]
            if rowParentSrl != 0 and (not row["visited"]):
                self.parentDepthFirstSearch(i)

    def parentDepthFirstSearch(self, rowIndex: int) -> int:
        self.tableReset[rowIndex]["visited"] = True

        parentSrl = self.tableReset[rowIndex]["parent_srl"]
        parentIndex = self.getIndexBySrl(parentSrl)
        if parentIndex == -1 :
            print(f"Parent srl {parentSrl} not found... Return 0. From {self.parentDepthFirstSearch.__name__}.")
            return 0

        parentRow = self.tableReset[parentIndex]

        if parentRow["parent_srl"] != 0:
            searchedParentSrl = self.parentDepthFirstSearch(parentIndex)
            self.tableReset[rowIndex]["parent_srl"] = searchedParentSrl
            return searchedParentSrl
        else:
            return parentRow["comment_srl"]

    def getIndexBySrl(self, srl: int) -> int:
        for i, row in enumerate(self.tableReset):
            if row["comment_srl"] == srl:
                return i
        return -1

    def updateComment(self, pulledCommentTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.updateCommentQuery, pulledCommentTable)
        self.dbController.getDB().commit()

    def pullParent(self) -> None:
        self.tableReset = self.selectComment()
        pulledCommentTable = self.pullUpParentSrl()
        self.updateComment(pulledCommentTable)
