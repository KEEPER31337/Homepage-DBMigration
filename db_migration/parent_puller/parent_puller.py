from typedef.typedef import Table
from db_controller.db_controller import DBController


class ParentPuller:
    dbController: DBController

    parentPulledTable: Table

    tableNameParentPull: str
    tableSrlCol: str
    parentSrlCol: str

    selectParentPulledFormat = (
        "SELECT {tableSrlCol}, {parentSrlCol}"
        " FROM {tableNameParentPull};")

    updateParentPulledFormat = (
        "UPDATE {tableNameParentPull}"
        " SET {parentSrlCol}=%({parentSrlCol})s"
        " WHERE {tableSrlCol}=%({tableSrlCol})s;")

    def __init__(self,
                 tableNameParentPull: str = "xe_comments",
                 tableSrlCol: str = "comment_srl",
                 parentSrlCol: str = "parent_srl") -> None:
        self.tableNameParentPull = tableNameParentPull
        self.parentSrlCol = parentSrlCol
        self.tableSrlCol = tableSrlCol

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def pullParent(self) -> None:
        self.parentPulledTable = self.selectParentPulled()
        self.initVisited()
        pulledTable = self.travelParentPulledTable()
        self.updateParentPulled(pulledTable)

    def selectParentPulled(self) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.formatSelectParentPulledQuery())
        return cursor.fetchall()

    def formatSelectParentPulledQuery(self) -> str:
        return self.selectParentPulledFormat.format(
            tableNameParentPull=self.tableNameParentPull,
            tableSrlCol=self.tableSrlCol,
            parentSrlCol=self.parentSrlCol)

    def initVisited(self):
        for i in range(len(self.parentPulledTable)):
            self.parentPulledTable[i]["visited"] = False

    def travelParentPulledTable(self) -> Table:

        for i, row in enumerate(self.parentPulledTable):
            rowParentSrl = row[self.parentSrlCol]
            if rowParentSrl != 0 and (not row["visited"]):
                print(row[self.tableSrlCol])
                self.searchPullParent(i)

        return self.parentPulledTable

    def searchPullParent(self, rowIndex: int) -> int:
        self.parentPulledTable[rowIndex]["visited"] = True

        parentSrl = self.parentPulledTable[rowIndex][self.parentSrlCol]
        rowSrl = self.parentPulledTable[rowIndex][self.tableSrlCol]
        # TODO : raise 화
        if parentSrl == rowSrl:
            print(
                f"Parent srl {parentSrl} and this row srl {rowSrl} is equal!"
                f" To avoid inf loop, return and set parent srl 0."
                f" From {self.searchPullParent.__name__}.")
            self.parentPulledTable[rowIndex][self.parentSrlCol] = 0
            return 0

        parentIndex = self.getIndexBySrl(parentSrl)
        # TODO : raise 화
        if parentIndex == -1:
            print(
                f"Parent srl {parentSrl} not found..."
                f" Return and set parent srl 0."
                f" From {self.searchPullParent.__name__}.")
            self.parentPulledTable[rowIndex][self.parentSrlCol] = 0
            return 0

        parentRow = self.parentPulledTable[parentIndex]

        if parentRow[self.parentSrlCol] != 0:
            searchedParentSrl = self.searchPullParent(parentIndex)
            self.parentPulledTable[rowIndex][self.parentSrlCol] = searchedParentSrl
            return searchedParentSrl
        else:
            return parentRow[self.tableSrlCol]

    def getIndexBySrl(self, srl: int) -> int:
        for i, row in enumerate(self.parentPulledTable):
            if row[self.tableSrlCol] == srl:
                return i
        return -1

    def updateParentPulled(self, pulledTable: Table) -> None:
        print(len(pulledTable))
        self.dbController.getCursor().executemany(
            self.formatUpdateParentPulledQuery(), pulledTable)
        self.dbController.getDB().commit()

    def formatUpdateParentPulledQuery(self) -> str:
        return self.updateParentPulledFormat.format(
            tableNameParentPull=self.tableNameParentPull,
            tableSrlCol=self.tableSrlCol,
            parentSrlCol=self.parentSrlCol)
