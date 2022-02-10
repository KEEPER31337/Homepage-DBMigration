from group_seperator.group_seperator import GroupSeperator
from typedef.typedef import Table


class JobSeperator(GroupSeperator):

    groupSrlCol = "member_job_id"
    defaultJobId: int

    insertJobQueryFormat = (
        "INSERT INTO member_has_member_job(member_id, member_job_id)"
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

    def selectMemberSrlTable(self) -> Table:
        cursor = self.oldDBController.getCursor()
        cursor.execute(self.getSelectMemberSrlQuery())

        memberSrlTable = cursor.fetchall()
        return memberSrlTable

    def setDefaultJobId(self, id: int) -> None:
        self.defaultJobId = id

    def getDefaultJobTable(self) -> Table:
        memberSrlTable = self.selectMemberSrlTable()
        for i in enumerate(memberSrlTable):
            memberSrlTable[i][self.groupSrlCol] = self.defaultJobId

        return memberSrlTable

    def getEditedJobTable(self) -> Table:
        return self.getEditedGroupTable() + self.getDefaultJobTable()

    def insertJobTable(self) -> None:
        cursor = self.newDBController.getCursor()

        cursor.executemany(
            self.getInsertJobQuery(),
            self.getEditedJobTable()
        )
        self.newDBController.getDB().commit()

    def seperateJob(self) -> None:
        self.insertJobTable()
