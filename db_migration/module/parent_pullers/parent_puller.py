from util.typedef import Table
from util.err import ParentSrlEqualError, ParentSrlNotFoundError
from util.db_controller import DBController


class ParentPuller:

    __parentPulledTable: Table

    __tableNameParentPull: str
    __tableSrlCol: str
    __parentSrlCol: str

    __selectParentPulledFormat = (
        "SELECT {tableSrlCol}, {parentSrlCol}"
        " FROM {tableNameParentPull};")

    __updateParentPulledFormat = (
        "UPDATE {tableNameParentPull}"
        " SET {parentSrlCol}=%({parentSrlCol})s"
        " WHERE {tableSrlCol}=%({tableSrlCol})s;")

    def __init__(self,
                 tableNameParentPull: str = "xe_comments",
                 tableSrlCol: str = "comment_srl",
                 parentSrlCol: str = "parent_srl") -> None:
        self.__tableNameParentPull = tableNameParentPull
        self.__parentSrlCol = parentSrlCol
        self.__tableSrlCol = tableSrlCol

    def pullParent(self) -> None:
        self.__parentPulledTable = self.__selectParentPulled()
        self.__initVisited()
        pulledTable = self.__travelParentPulledTable()
        self.__updateParentPulled(pulledTable)

    def __selectParentPulled(self) -> Table:
        cursor = self._dbController.getCursor()
        cursor.execute(self.__formatSelectParentPulledQuery())
        return cursor.fetchall()

    def __formatSelectParentPulledQuery(self) -> str:
        return self.__selectParentPulledFormat.format(
            tableNameParentPull=self.__tableNameParentPull,
            tableSrlCol=self.__tableSrlCol,
            parentSrlCol=self.__parentSrlCol)

    def __initVisited(self):
        for i in range(len(self.__parentPulledTable)):
            self.__parentPulledTable[i]["visited"] = False

    def __travelParentPulledTable(self) -> Table:

        for i, row in enumerate(self.__parentPulledTable):
            rowParentSrl = row[self.__parentSrlCol]
            if rowParentSrl != 0 and not row["visited"]:
                self.__searchPullParent(i)

        return self.__parentPulledTable

    def __searchPullParent(self, rowIndex: int) -> int:
        self.__parentPulledTable[rowIndex]["visited"] = True

        parentSrl = self.__parentPulledTable[rowIndex][self.__parentSrlCol]
        rowSrl = self.__parentPulledTable[rowIndex][self.__tableSrlCol]

        try:
            if parentSrl == rowSrl:
                raise ParentSrlEqualError(
                    className=self.__class__.__name__,
                    methodName=self.__searchPullParent.__name__,
                    parentSrl=parentSrl,
                    rowSrl=rowSrl,
                    msg="To avoid infinite loop, return and set parent srl 0.")
        except ParentSrlEqualError as ee:
            print(ee)
            self.__parentPulledTable[rowIndex][self.__parentSrlCol] = 0
            return 0

        parentIndex = self.__getIndexBySrl(parentSrl)

        try:
            if parentIndex == -1:
                raise ParentSrlNotFoundError(
                    className=self.__class__.__name__,
                    methodName=self.__searchPullParent.__name__,
                    parentSrl=parentSrl,
                    msg="Return and set parent srl 0.")

        except ParentSrlNotFoundError as nfe:
            print(nfe)
            self.__parentPulledTable[rowIndex][self.__parentSrlCol] = 0
            return 0

        parentRow = self.__parentPulledTable[parentIndex]

        if parentRow[self.__parentSrlCol] != 0:
            searchedParentSrl = self.__searchPullParent(parentIndex)
            self.__parentPulledTable[rowIndex][self.__parentSrlCol] = searchedParentSrl
            return searchedParentSrl
        else:
            return parentRow[self.__tableSrlCol]

    def __getIndexBySrl(self, srl: int) -> int:
        for i, row in enumerate(self.__parentPulledTable):
            if row[self.__tableSrlCol] == srl:
                return i
        return -1

    def __updateParentPulled(self, pulledTable: Table) -> None:
        self._dbController.getCursor().executemany(
            self.__formatUpdateParentPulledQuery(), pulledTable)
        self._dbController.getDB().commit()

    def __formatUpdateParentPulledQuery(self) -> str:
        return self.__updateParentPulledFormat.format(
            tableNameParentPull=self.__tableNameParentPull,
            tableSrlCol=self.__tableSrlCol,
            parentSrlCol=self.__parentSrlCol)
