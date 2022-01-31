from typing import Dict, List, Union
from multipledispatch import dispatch
from db_controller.db_controller import DBController


class GroupSeperator:
    oldDBController: DBController
    newDBController: DBController

    oldGroupSrlDict: Dict[str, int]
    newGroupSrlDict: Dict[str, int]

    selectGroupSrlQueryFormat = (
        "SELECT t1.member_srl AS {memberSrlCol}, t2.group_srl AS {groupSrlCol}, t2.title AS {groupTitleCol}"
        " FROM xe_member_group_member as t1, xe_member_group as t2"
        " WHERE (t1.group_srl = t2.group_srl AND"
        " t1.group_srl IN("
    )

    memberSrlCol = "member_id"
    groupSrlCol = "group_id"
    groupTitleCol = "group_name"

    @dispatch()
    def __init__(self) -> None:
        self.oldGroupSrlDict = dict()
        self.newGroupSrlDict = dict()

    @dispatch(str)
    def __init__(self, groupSrlCol: str) -> None:
        self.oldGroupSrlDict = dict()
        self.newGroupSrlDict = dict()
        
        self.groupSrlCol = groupSrlCol

    @dispatch(str, str, str)
    def __init__(self, memberSrlCol: str, groupSrlCol: str, groupTitleCol: str) -> None:
        self.oldGroupSrlDict = dict()
        self.newGroupSrlDict = dict()

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

    def updateGroupTable(self, 
        oldGroupTable: List[Dict[str, Union[int, str]]]) -> List[Dict[str, Union[int, str]]]:
        newGroupTable = oldGroupTable

        for i, d in enumerate(newGroupTable):
            job = d[self.groupTitleCol]
            newGroupTable[i][self.groupSrlCol] = self.newGroupSrlDict[job]

        return newGroupTable
    
    def getGroupTable(self) -> List[Dict[str, Union[int, str]]]: 
        return self.updateGroupTable(self.selectGroupTable(self.oldDBController))

    def selectGroupTable(self, oldDB: DBController) -> List[Dict[str, Union[int, str]]]:
        cursor = oldDB.getCursor()
        cursor.execute(
            self.getSelectGroupSrlQuery(),
            self.getOldSrlData()
        )

        oldGroupTable:List[Dict[str, Union[int, str]]] = cursor.fetchall()

        return oldGroupTable
