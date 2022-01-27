from typing import Dict, List, Union
from multipledispatch import dispatch
from db_controller.db_controller import DBController


class GroupSeperator:
    oldDBController: DBController
    newDBController: DBController

    oldGroupSrlDict: Dict[str, int] = dict()
    newGroupSrlDict: Dict[str, int] = dict()

    selectGroupSrlQueryFormat = (
        "SELECT t1.member_srl AS {memberSrlCol}, t2.group_srl AS {groupSrlCol}, t2.title AS {groupTitleCol}"
        " FROM xe_member_group_member as t1, xe_member_group as t2"
        " WHERE (t1.group_srl = t2.group_srl AND"
        " t1.group_srl IN("
    )

    memberSrlCol = "member_id"
    groupSrlCol = "group_id"
    groupTitleCol = "group_name"

    oldGroupTable: List[Dict[str, Union[int, str]]] = list()
    newGroupTable: List[Dict[str, Union[int, str]]] = list()

    @dispatch()
    def __init__(self) -> None:
        # Columns are set as default value.
        print("init void")
        # pass

    @dispatch(str)
    def __init__(self, groupSrlCol: str) -> None:
        self.groupSrlCol = groupSrlCol

    @dispatch(str, str, str)
    def __init__(self, memberSrlCol: str, groupSrlCol: str, groupTitleCol: str) -> None:
        self.memberSrlCol = memberSrlCol
        self.groupSrlCol = groupSrlCol
        self.groupTitleCol = groupTitleCol

    def setOldDBController(self, dbController: DBController):
        self.oldDBController = dbController

    def setNewDBController(self, dbController: DBController):
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

    def updateGroupTable(self) -> List[Dict[str, Union[int, str]]]:
        tmp = self.oldGroupTable

        for i, d in enumerate(tmp):
            job = d[self.groupTitleCol]
            tmp[i][self.groupSrlCol] = self.newGroupSrlDict[job]

        self.newGroupTable = tmp
        print(self.newGroupTable)
        return self.newGroupTable

    def selectGroupTable(self, oldDB: DBController) -> List[Dict[str, Union[int, str]]]:
        cursor = oldDB.getCursor()
        cursor.execute(
            self.getSelectGroupSrlQuery(),
            self.getOldSrlData()
        )

        self.oldGroupTable = cursor.fetchall()

        return self.oldGroupTable
