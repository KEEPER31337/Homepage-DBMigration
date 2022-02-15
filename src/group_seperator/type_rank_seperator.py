from abc import ABCMeta, abstractclassmethod
from typedef.typedef import Table
from group_seperator.group_seperator import GroupSeperator


class TypeRankSeperator(GroupSeperator, metaclass=ABCMeta):

    typeRankIdCol: str

    updateTypeRankFormat = (
        "UPDATE member"
        " SET {typeRankIdCol} = %({groupSrlCol})s"
        " WHERE id = %({memberSrlCol})s;")

    @abstractclassmethod
    def __init__(self,
                 memberSrlCol: str,
                 groupSrlCol: str,
                 groupTitleCol: str,
                 typeRankIdCol: str) -> None:

        self.typeRankIdCol = typeRankIdCol

        super().__init__(memberSrlCol, groupSrlCol, groupTitleCol)

    def formatUpdateTypeRankQuery(self) -> str:
        return self.updateTypeRankFormat.format(
            typeRankIdCol=self.typeRankIdCol,
            memberSrlCol=self.memberSrlCol,
            groupSrlCol=self.groupSrlCol)

    def updateTypeRank(self, typeRankSrlTable: Table) -> None:
        cursor = self.newDBController.getCursor()
        cursor.executemany(
            self.formatUpdateTypeRankQuery(),
            typeRankSrlTable
        )
        self.newDBController.getDB().commit()

    def selectTypeRankSrl(self) -> Table:
        return self.selectGroupSrl()

    def getEditedTypeRankSrlTable(self, typeRankSrlTable: Table) -> Table:
        return self.getEditedGroupSrlTable(typeRankSrlTable)

    def seperateTypeRank(self) -> None:
        typeRankSrlTable = self.selectTypeRankSrl()
        editedTypeRankSrlTable = self.getEditedTypeRankSrlTable(
            typeRankSrlTable)
        self.updateTypeRank(editedTypeRankSrlTable)
