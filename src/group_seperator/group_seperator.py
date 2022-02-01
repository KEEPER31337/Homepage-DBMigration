from typing import Dict, List
from db_controller.db_controller import DBController
from utils.typedef import Table


class GroupSeperator:
    oldDBController: DBController
    newDBController: DBController

    oldGroupSrlDict: Dict[str, int]
    newGroupSrlDict: Dict[str, int]

    memberSrlCol: str
    groupSrlCol: str
    groupTitleCol: str

    selectGroupSrlQueryFormat = (
        "SELECT t1.member_srl AS {memberSrlCol}, t2.group_srl AS {groupSrlCol}, t2.title AS {groupTitleCol}"
        " FROM xe_member_group_member as t1, xe_member_group as t2"
        " WHERE (t1.group_srl = t2.group_srl AND"
        " t1.group_srl IN(")

    def __init__(self,
                 memberSrlCol: str = "member_id",
                 groupSrlCol: str = "group_id",
                 groupTitleCol: str = "group_name") -> None:
        self.oldGroupSrlDict = dict()
        self.newGroupSrlDict = dict()

        self.memberSrlCol = memberSrlCol
        self.groupSrlCol = groupSrlCol
        self.groupTitleCol = groupTitleCol

    def setOldDBController(self, dbController: DBController) -> None:
        self.oldDBController = dbController

    def setNewDBController(self, dbController: DBController) -> None:
        self.newDBController = dbController

    def addGroupSrl(self, groupName: str, oldSrl: int, newSrl: int) -> None:
        self.oldGroupSrlDict[groupName] = oldSrl
        self.newGroupSrlDict[groupName] = newSrl

    def formatSelectGroupQuery(self) -> str:
        return self.selectGroupSrlQueryFormat.format(
            memberSrlCol=self.memberSrlCol,
            groupSrlCol=self.groupSrlCol,
            groupTitleCol=self.groupTitleCol)

    def getSelectGroupConditionFormat(self) -> str:
        conditionFormat = "%s"
        for i in range(len(self.oldGroupSrlDict)-1):
            conditionFormat += ",%s"
        conditionFormat += "));"

        return conditionFormat

    def getSelectGroupSrlQuery(self) -> str:
        return self.formatSelectGroupQuery() + self.getSelectGroupConditionFormat()

    def getOldSrlData(self) -> List[int]:
        return list(self.oldGroupSrlDict.values())

    def editGroupTable(self, oldGroupTable: Table) -> Table:
        newGroupTable = oldGroupTable

        for i, d in enumerate(newGroupTable):
            job = d[self.groupTitleCol]
            newGroupTable[i][self.groupSrlCol] = self.newGroupSrlDict[job]

        return newGroupTable

    def getEditedGroupTable(self) -> Table:
        return self.editGroupTable(self.selectGroupTable())

    def selectGroupTable(self) -> Table:
        cursor = self.oldDBController.getCursor()
        cursor.execute(
            self.getSelectGroupSrlQuery(),
            self.getOldSrlData()
        )

        oldGroupTable: Table = cursor.fetchall()

        return oldGroupTable
