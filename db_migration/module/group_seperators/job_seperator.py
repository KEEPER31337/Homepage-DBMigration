from util.typedef import Table
from module.interface import FormatInterface
from module.group_seperators.group_seperator import GroupSeperator


class JobSeperator(GroupSeperator, FormatInterface):

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
        cursor.execute(self._formatQuery(self.__selectMemberSrlFormat))

        memberSrlTable = cursor.fetchall()
        return memberSrlTable

    def _formatQuery(self, queryFormat: str) -> str:
        return queryFormat.format(
            memberSrlCol=self._memberSrlCol,
            groupSrlCol=self._groupSrlCol)

    def __getDefaultJobTable(self, memberSrlTable: Table) -> Table:
        for i in range(len(memberSrlTable)):
            memberSrlTable[i][self._groupSrlCol] = self.__defaultJobId

        return memberSrlTable

    def __insertJob(self, jobTable: Table) -> None:
        cursor = self._newDBController.getCursor()

        # pymysql.err.IntegrityError : FK 비일치
        cursor.executemany(
            self._formatQuery(self.__insertJobFormat),
            jobTable
        )
        self._newDBController.getDB().commit()
