from group_seperator.group_seperator import GroupSeperator, Table
from db_controller.db_controller import DBController


class JobSeperator(GroupSeperator):

    groupSrlCol = "member_job_id"
    defaultJobId: int

    insertJobQueryFormat = (
        "INSERT INTO test"
        " VALUES(%({memberSrlCol})s,%({groupSrlCol})s);")

    selectMemberSrlQuery = (
        "SELECT member_srl AS {memberSrlCol}"
        " FROM xe_member;")

    def getInsertJobQuery(self) -> str:
        return self.insertJobQueryFormat.format(
            memberSrlCol=self.memberSrlCol,
            groupSrlCol=self.groupSrlCol)

    def getSelectMemberSrlQuery(self) -> str:
        return self.selectMemberSrlQuery.format(
            memberSrlCol=self.memberSrlCol
        )

    def selectMemberSrlTable(self, oldDB: DBController) -> Table:
        cursor = oldDB.getCursor()
        cursor.execute(self.getSelectMemberSrlQuery())

        memberSrlTable = cursor.fetchall()
        return memberSrlTable

    def setDefaultJobId(self, id: int) -> None:
        self.defaultJobId = id

    def getDefaultJobTable(self) -> Table:
        memberSrlTable = self.selectMemberSrlTable(self.newDBController)
        for i in enumerate(memberSrlTable):
            memberSrlTable[i][self.groupSrlCol] = self.defaultJobId

        return memberSrlTable

    def getJobSeperateTable(self) -> Table:
        return self.getGroupTable() + self.getDefaultJobTable()

    def insertJobTable(self, newDB: DBController) -> None:
        cursor = newDB.getCursor()

        cursor.executemany(
            self.getInsertJobQuery(),
            self.getJobSeperateTable()
        )
        newDB.getDB().commit()

    def seperateJob(self) -> None:
        self.selectGroupTable(self.oldDBController)
        self.insertJobTable(self.newDBController)
