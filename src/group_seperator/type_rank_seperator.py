from group_seperator.group_seperator import GroupSeperator
from src.db_controller.db_controller import DBController


class TypeRankSeperator(GroupSeperator):

    typeRankIdCol = ""
    updateTypeRankQueryFormat = ("UPDATE member"
                                 " SET {typeRankIdCol} = %({groupSrlCol})s"
                                 " WHERE id = %({memberSrlCol})s;")

    def getUpdateTypeRankQuery(self) -> str:
        return self.updateTypeRankQueryFormat.format(
            typeRankIdCol=self.typeRankIdCol,
            memberSrlCol=self.memberSrlCol,
            groupSrlCol=self.groupSrlCol)

    def updateTypeRankTable(self, newDB: DBController) -> None:
        cursor = newDB.getCursor()
        cursor.executemany(
            self.getUpdateTypeRankQuery(),
            self.updateGroupTable()
        )
        newDB.getDB().commit()