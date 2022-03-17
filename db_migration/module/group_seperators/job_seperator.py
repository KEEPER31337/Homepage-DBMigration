from util.typedef import Table
from module.group_seperators.group_seperator import GroupSeperator


class JobSeperator(GroupSeperator):

    __defaultJobId: int

    __insertJobFormat = (
        "INSERT INTO member_has_member_job(member_id, member_job_id)"
        " VALUES(%({memberSrlCol})s,%({groupSrlCol})s);")

    __selectMemberSrlFormat = (
        "SELECT member_srl AS {memberSrlCol}"
        " FROM xe_member;")

    def __init__(self,
                 memberSrlCol: str = "member_id",
                 jobSrlCol: str = "member_job_id",
                 jobTitleCol: str = "job_name") -> None:

        super().__init__(memberSrlCol, jobSrlCol, jobTitleCol)

    def setDefaultJobId(self, id: int) -> None:
        self.__defaultJobId = id

    def seperateJob(self) -> None:
        jobSrlTable = self.__selectJobSrl()
        editedJobSrlTable = self.__getEditedJobSrlTable(jobSrlTable)

        memberSrlTable = self.__selectMemberSrl()
        defaultJobTable = self.__getDefaultJobTable(memberSrlTable)

        jobTable = editedJobSrlTable + defaultJobTable
        self.__insertJob(jobTable)

    def __selectJobSrl(self) -> Table:
        return self._selectGroupSrl()

    def __getEditedJobSrlTable(self, jobSrlTable: Table) -> Table:
        return self._getEditedGroupSrlTable(jobSrlTable)

    def __selectMemberSrl(self) -> Table:
        cursor = self._oldDBController.getCursor()
        cursor.execute(self.__formatSelectMemberSrlQuery())

        memberSrlTable = cursor.fetchall()
        return memberSrlTable

    def __formatSelectMemberSrlQuery(self) -> str:
        return self.__selectMemberSrlFormat.format(
            memberSrlCol=self._memberSrlCol)

    def __getDefaultJobTable(self, memberSrlTable: Table) -> Table:
        for i in range(len(memberSrlTable)):
            memberSrlTable[i][self._groupSrlCol] = self.__defaultJobId

        return memberSrlTable

    def __insertJob(self, jobTable: Table) -> None:
        cursor = self._newDBController.getCursor()

        # pymysql.err.IntegrityError : FK 비일치
        cursor.executemany(
            self.__formatInsertJobQuery(),
            jobTable
        )
        self._newDBController.getDB().commit()

    def __formatInsertJobQuery(self) -> str:
        return self.__insertJobFormat.format(
            memberSrlCol=self._memberSrlCol,
            groupSrlCol=self._groupSrlCol)
