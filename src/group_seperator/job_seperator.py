from group_seperator.group_seperator import GroupSeperator
from typedef.typedef import Table


class JobSeperator(GroupSeperator):

    defaultJobId: int

    insertJobFormat = (
        "INSERT INTO member_has_member_job(member_id, member_job_id)"
        " VALUES(%({memberSrlCol})s,%({groupSrlCol})s);")

    selectMemberSrlFormat = (
        "SELECT member_srl AS {memberSrlCol}"
        " FROM xe_member;")

    def __init__(self,
                 memberSrlCol: str = "member_id",
                 jobSrlCol: str = "member_job_id",
                 jobTitleCol: str = "job_name") -> None:
        super().__init__(memberSrlCol, jobSrlCol, jobTitleCol)

    def formatInsertJobQuery(self) -> str:
        return self.insertJobFormat.format(
            memberSrlCol=self.memberSrlCol,
            groupSrlCol=self.groupSrlCol)

    def formatSelectMemberSrlQuery(self) -> str:
        return self.selectMemberSrlFormat.format(
            memberSrlCol=self.memberSrlCol
        )

    def selectMemberSrlTable(self) -> Table:
        cursor = self.oldDBController.getCursor()
        cursor.execute(self.formatSelectMemberSrlQuery())

        memberSrlTable = cursor.fetchall()
        return memberSrlTable

    def setDefaultJobId(self, id: int) -> None:
        self.defaultJobId = id

    def getDefaultJobTable(self, memberSrlTable: Table) -> Table:
        for i in enumerate(memberSrlTable):
            memberSrlTable[i][self.groupSrlCol] = self.defaultJobId

        return memberSrlTable

    def insertJobTable(self, jobTable: Table) -> None:
        cursor = self.newDBController.getCursor()

        cursor.executemany(
            self.formatInsertJobQuery(),
            jobTable
        )
        self.newDBController.getDB().commit()

    def selectJobSrlTable(self) -> Table:
        return self.selectGroupSrlTable()

    def getEditedJobSrlTable(self, jobSrlTable: Table) -> Table:
        return self.getEditedGroupSrlTable(jobSrlTable)

    def seperateJob(self) -> None:
        jobSrlTable = self.selectJobSrlTable()
        editedJobSrlTable = self.getEditedJobSrlTable(jobSrlTable)

        memberSrlTable = self.selectMemberSrlTable()
        defaultJobTable = self.getDefaultJobTable(memberSrlTable)

        jobTable = editedJobSrlTable + defaultJobTable
        self.insertJobTable(jobTable)
