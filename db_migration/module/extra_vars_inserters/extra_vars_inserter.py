# Add student number columns, parse extra_vars column and update rows.

from module.interface import DBControllInterface
from util.err import DuplicatedColumnExistErrorLog
from util.typedef import Table
from pymysql import OperationalError
from module.extra_vars_inserters.extra_vars_parser import ExtraVarsParser


class ExtraVarsInserter(DBControllInterface):

    __addStudentNumberColumnQuery = (
        "ALTER TABLE xe_member"
        " ADD student_number VARCHAR(45) DEFAULT NULL")

    __selectMemberQuery = (
        "SELECT member_srl, extra_vars"
        " FROM `xe_member`;")

    __updateMemberQuery = (
        "UPDATE xe_member"
        " SET student_number = %(student_number)s"
        " WHERE member_srl = %(member_srl)s;")

    def insertExtraVars(self) -> None:
        self.__addExtraVarsColumns()
        memberTable = self.__selectMember()
        appendedMemberTable = self.__appendParsedExtraVars(memberTable)
        self.__updateMemberTable(appendedMemberTable)

    def __addExtraVarsColumns(self) -> None:
        try:
            self._dbController.getCursor().execute(self.__addStudentNumberColumnQuery)
        except OperationalError as oe:
            print(DuplicatedColumnExistErrorLog(
                err=oe,
                className=self.__class__.__name__,
                methodName=self.__addExtraVarsColumns.__name__,
                columnName="student_number"))

    def __selectMember(self) -> Table:
        cursor = self._dbController.getCursor()
        cursor.execute(self.__selectMemberQuery)
        memberTable = cursor.fetchall()
        return memberTable

    def __appendParsedExtraVars(self, memberTable: Table) -> Table:
        for i, row in enumerate(memberTable):
            parsedExtraVars = ExtraVarsParser.parseExtraVars(row['extra_vars'])
            memberTable[i].update(parsedExtraVars)

        return memberTable

    def __updateMemberTable(self, appendedMemberTable: Table) -> None:
        self._dbController.getCursor().executemany(
            self.__updateMemberQuery, appendedMemberTable)
        self._dbController.getDB().commit()
