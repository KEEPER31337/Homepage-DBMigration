# Add student number columns, parse extra_vars column and update rows.

from db_controller.db_controller import DBController
from extra_vars_extractor.extra_vars_parser import ExtraVarsParser
from shared.typedef import Table


class ExtraVarsInserter:
    addStudentNumberColumnQuery = (
        "ALTER TABLE xe_member"
        " ADD student_number VARCHAR(45) DEFAULT NULL")

    selectMemberQuery = (
        "SELECT member_srl, extra_vars"
        " FROM `xe_member`;")

    updateMemberQuery = (
        "UPDATE xe_member"
        " SET student_number = %(student_number)s"
        " WHERE member_srl = %(member_srl)s;")

    dbController: DBController

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def addColumns(self) -> None:
        self.dbController.getCursor().execute(self.addStudentNumberColumnQuery)

    def selectMemberTable(self) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectMemberQuery)
        memberTable = cursor.fetchall()
        return memberTable

    def appendParsedExtraVars(self, memberTable: Table) -> Table:
        for i, row in enumerate(memberTable):
            print(f"Member serial : {row['member_srl']}")
            parsedExtraVars = ExtraVarsParser.parseExtraVars(row['extra_vars'])
            print()
            memberTable[i].update(parsedExtraVars)

        return memberTable

    def getAppendedMemberTable(self) -> Table:
        return self.appendParsedExtraVars(self.selectMemberTable())

    def updateMemberRows(self) -> None:
        self.dbController.getCursor().executemany(
            self.updateMemberQuery, self.getAppendedMemberTable())
        self.dbController.getDB().commit()

    def insertExtraVars(self) -> None:
        self.addColumns()
        self.updateMemberRows()
