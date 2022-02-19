from abc import ABCMeta, abstractclassmethod
from typing import List
from typedef.typedef import Row, Table
from db_controller.db_controller import DBController


class GroupSeperator(metaclass=ABCMeta):
    oldDBController: DBController
    newDBController: DBController

    oldGroupSrlDict: Row
    newGroupSrlDict: Row

    memberSrlCol: str
    groupSrlCol: str
    groupTitleCol: str

    selectGroupSrlFormat = (
        "SELECT t1.member_srl AS {memberSrlCol}, t2.group_srl AS {groupSrlCol}, t2.title AS {groupTitleCol}"
        " FROM xe_member_group_member as t1, xe_member_group as t2"
        " WHERE (t1.group_srl = t2.group_srl AND"
        " t1.group_srl IN(")

    def __init__(self,
                 memberSrlCol: str,
                 groupSrlCol: str,
                 groupTitleCol: str) -> None:

        self.memberSrlCol = memberSrlCol
        self.groupSrlCol = groupSrlCol
        self.groupTitleCol = groupTitleCol

        self.oldGroupSrlDict = dict()
        self.newGroupSrlDict = dict()

    def setOldDBController(self, dbController: DBController) -> None:
        self.oldDBController = dbController

    def setNewDBController(self, dbController: DBController) -> None:
        self.newDBController = dbController

    def addGroupSrlDict(self, groupName: str, oldSrl: int, newSrl: int) -> None:
        self.oldGroupSrlDict[groupName] = oldSrl
        self.newGroupSrlDict[groupName] = newSrl

    def formatSelectGroupSrlQuery(self) -> str:
        return self.selectGroupSrlFormat.format(
            memberSrlCol=self.memberSrlCol,
            groupSrlCol=self.groupSrlCol,
            groupTitleCol=self.groupTitleCol)

    def getGroupConditionFormat(self) -> str:
        conditionFormat = "%s"
        for i in range(len(self.oldGroupSrlDict)-1):
            conditionFormat += ",%s"
        conditionFormat += "));"

        return conditionFormat

    def getSelectGroupSrlQuery(self) -> str:
        return self.formatSelectGroupSrlQuery() + self.getGroupConditionFormat()

    def getOldSrlData(self) -> List[int]:
        return list(self.oldGroupSrlDict.values())

    def getEditedGroupSrlTable(self, groupSrlTable: Table) -> Table:
        for i, row in enumerate(groupSrlTable):
            group = row[self.groupTitleCol]
            groupSrlTable[i][self.groupSrlCol] = self.newGroupSrlDict[group]

        return groupSrlTable

    def selectGroupSrl(self) -> Table:
        cursor = self.oldDBController.getCursor()
        cursor.execute(
            self.getSelectGroupSrlQuery(),
            self.getOldSrlData()
        )

        oldGroupTable: Table = cursor.fetchall()

        return oldGroupTable
