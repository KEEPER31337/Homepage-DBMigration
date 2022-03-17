from abc import ABCMeta
from typing import List
from util.typedef import Row, Table
from util.db_controller import DBController


class GroupSeperator(metaclass=ABCMeta):
    _oldDBController: DBController
    _newDBController: DBController

    __oldGroupSrlDict: Row
    __newGroupSrlDict: Row

    _memberSrlCol: str
    _groupSrlCol: str
    _groupTitleCol: str

    selectGroupSrlFormat = (
        "SELECT t1.member_srl AS {memberSrlCol}, t2.group_srl AS {groupSrlCol}, t2.title AS {groupTitleCol}"
        " FROM xe_member_group_member as t1, xe_member_group as t2"
        " WHERE (t1.group_srl = t2.group_srl AND"
        " t1.group_srl IN(")

    def __init__(self,
                 memberSrlCol: str,
                 groupSrlCol: str,
                 groupTitleCol: str) -> None:

        self._memberSrlCol = memberSrlCol
        self._groupSrlCol = groupSrlCol
        self._groupTitleCol = groupTitleCol

        self.__oldGroupSrlDict = dict()
        self.__newGroupSrlDict = dict()

    def setOldDBController(self, dbController: DBController) -> None:
        self._oldDBController = dbController

    def setNewDBController(self, dbController: DBController) -> None:
        self._newDBController = dbController

    def addGroupSrlDict(self, groupName: str, oldSrl: int, newSrl: int) -> None:
        self.__oldGroupSrlDict[groupName] = oldSrl
        self.__newGroupSrlDict[groupName] = newSrl

    def _selectGroupSrl(self) -> Table:
        cursor = self._oldDBController.getCursor()
        cursor.execute(
            self.__getSelectGroupSrlQuery(),
            self.__getOldSrlData()
        )

        oldGroupTable: Table = cursor.fetchall()

        return oldGroupTable

    def __getSelectGroupSrlQuery(self) -> str:
        return f"{self.__formatSelectGroupSrlQuery()}{self.__getGroupConditionFormat()}"

    def __formatSelectGroupSrlQuery(self) -> str:
        return self.selectGroupSrlFormat.format(
            memberSrlCol=self._memberSrlCol,
            groupSrlCol=self._groupSrlCol,
            groupTitleCol=self._groupTitleCol)

    def __getGroupConditionFormat(self) -> str:
        conditionFormat = "%s"
        for _ in range(len(self.__oldGroupSrlDict)-1):
            conditionFormat += ",%s"
        conditionFormat += "));"

        return conditionFormat

    def __getOldSrlData(self) -> List[int]:
        return list(self.__oldGroupSrlDict.values())

    def _getEditedGroupSrlTable(self, groupSrlTable: Table) -> Table:
        for i, row in enumerate(groupSrlTable):
            group = row[self._groupTitleCol]
            groupSrlTable[i][self._groupSrlCol] = self.__newGroupSrlDict[group]

        return groupSrlTable
