
# Add student number columns, parse extra_vars column and update rows.

from db_controller.db_controller import DBController
from extra_vars_extractor.extra_vars_parser import ExtraVarsParser
from typing import Dict, List


class ExtraVarsInserter:
    addStudentNumberColumnQuery = "ALTER TABLE xe_member ADD student_number VARCHAR(45) DEFAULT NULL"
    selectMemberQuery = "SELECT member_srl, extra_vars FROM `xe_member`;"
    updateMemberQuery = "UPDATE xe_member SET student_number = %(student_number)s WHERE member_srl = %(member_srl)s;"

    dbController: DBController
    memberRows: List[Dict[str, str]]

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def addColumns(self) -> None:
        self.dbController.getCursor().execute(self.addStudentNumberColumnQuery)

    def selectMemberRows(self) -> List[Dict[str, str]]:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectMemberQuery)
        self.memberRows = cursor.fetchall()
        return self.memberRows

    def appendParsedExtraVars(self) -> List[Dict[str, str]]:
        for i, row in enumerate(self.memberRows):
            print(f"Member serial : {row['member_srl']}")
            parsedExtraVars = ExtraVarsParser.parseExtraVars(row['extra_vars'])
            print()
            self.memberRows[i].update(parsedExtraVars)

        return self.memberRows

    def updateMemberRows(self) -> None:
        self.dbController.getCursor().executemany(
            self.updateMemberQuery, self.memberRows)
        self.dbController.getDB().commit()

    def insertExtraVars(self) -> None:
        self.addColumns()
        self.selectMemberRows()
        self.appendParsedExtraVars()
        self.updateMemberRows()
