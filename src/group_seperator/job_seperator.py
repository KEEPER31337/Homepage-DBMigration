from src.group_seperator.group_seperator import GroupSeperator
from src.db_controller.db_controller import DBController


class JobSeperator(GroupSeperator):

    groupSrlCol = "member_job_id"
    insertJobQueryFormat = ("INSERT INTO test",
                            " VALUES(%({memberSrlCol})s,%({groupSrlCol})s);")

    def getInsertJobQuery(self) -> str:
        return self.insertJobQueryFormat.format(
            memberSrlCol=self.memberSrlCol,
            groupSrlCol=self.groupSrlCol)

    def insertJobTable(self, newDB: DBController) -> None:
        cursor = newDB.getCursor()
        cursor.executemany(
            self.getSelectGroupConditionFormat(),
            self.updateGroupTable()
        )
        newDB.getDB().commit()

    def seperateJob(self):
        self.selectGroupTable(self.oldDBController)
        self.insertJobTable(self.newDBController)
