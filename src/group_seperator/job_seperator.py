from typing import Dict, List, Union

from group_seperator.group_seperator import GroupSeperator
from db_controller.db_controller import DBController


class JobSeperator(GroupSeperator):

    groupSrlCol = "member_job_id"
    defaultJobId: int
    memberSrlTable: List[Dict[str, int]] = list()
    insertJobQueryFormat = ("INSERT INTO test"
                            " VALUES(%({memberSrlCol})s,%({groupSrlCol})s);")

    selectMemberSrlQuery = "SELECT member_srl AS {memberSrlCol} FROM xe_member;"

    def getInsertJobQuery(self) -> str:
        return self.insertJobQueryFormat.format(
            memberSrlCol=self.memberSrlCol,
            groupSrlCol=self.groupSrlCol)

    def getSelectMemberSrlQuery(self) -> str:
        return self.selectMemberSrlQuery.format(
            memberSrlCol=self.memberSrlCol
        )

    def selectMemberSrlTable(self, oldDB: DBController) -> List[Dict[str, int]]:
        cursor = oldDB.getCursor()
        cursor.execute(self.getSelectMemberSrlQuery())

        memberSrlTable = cursor.fetchall()
        return memberSrlTable

    def setDefaultJobId(self, id: int) -> None:
        self.defaultJobId = id

    def getDefaultJobData(self) -> List[Dict[str, int]]:
        memberSrlTable = self.selectMemberSrlTable()
        for i in enumerate(memberSrlTable):
            memberSrlTable[i][self.groupSrlCol] = self.defaultJobId

        return memberSrlTable

    def getJobSeperateData(self) -> List[Dict[str, Union[int, str]]]:
        return self.updateGroupTable() + self.getDefaultJobData()

    def insertJobTable(self, newDB: DBController) -> None:
        cursor = newDB.getCursor()

        cursor.executemany(
            self.getInsertJobQuery(),
            self.getJobSeperateData()
        )
        newDB.getDB().commit()

    def seperateJob(self) -> None:
        self.selectGroupTable(self.oldDBController)
        self.insertJobTable(self.newDBController)
