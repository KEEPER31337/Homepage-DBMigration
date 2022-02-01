from group_seperator.group_seperator import GroupSeperator


class TypeRankSeperator(GroupSeperator):

    typeRankIdCol: str
    updateTypeRankQueryFormat = (
        "UPDATE member"
        " SET {typeRankIdCol} = %({groupSrlCol})s"
        " WHERE id = %({memberSrlCol})s;")

    def getUpdateTypeRankQuery(self) -> str:
        return self.updateTypeRankQueryFormat.format(
            typeRankIdCol=self.typeRankIdCol,
            memberSrlCol=self.memberSrlCol,
            groupSrlCol=self.groupSrlCol)

    def updateTypeRankTable(self) -> None:
        cursor = self.newDBController.getCursor()
        cursor.executemany(
            self.getUpdateTypeRankQuery(),
            self.getEditedGroupTable()
        )
        self.newDBController.getDB().commit()
        
