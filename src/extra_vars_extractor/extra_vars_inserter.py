# Add student number columns, parse extra_vars column and update rows.

from typedef.typedef import Table
from pymysql import OperationalError
from db_controller.db_controller import DBController
from extra_vars_extractor.extra_vars_parser import ExtraVarsParser


class ExtraVarsInserter:
    dbController: DBController

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

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def addExtraVarsColumns(self) -> None:
        try:
            self.dbController.getCursor().execute(self.addStudentNumberColumnQuery)
        except OperationalError as oe:
            print(
                f"{oe} : There is a column already. From {self.addExtraVarsColumns.__name__}.")

    def selectMemberTable(self) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectMemberQuery)
        memberTable = cursor.fetchall()
        return memberTable

    def appendParsedExtraVars(self, memberTable: Table) -> Table:
        for i, row in enumerate(memberTable):
            parsedExtraVars = ExtraVarsParser.parseExtraVars(row['extra_vars'])
            memberTable[i].update(parsedExtraVars)

        return memberTable

    def updateMemberTable(self, appendedMemberTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.updateMemberQuery, appendedMemberTable)
        self.dbController.getDB().commit()

    def insertExtraVars(self) -> None:
        self.addExtraVarsColumns()
        memberTable = self.selectMemberTable()
        appendedMemberTable = self.appendParsedExtraVars(memberTable)
        self.updateMemberTable(appendedMemberTable)
