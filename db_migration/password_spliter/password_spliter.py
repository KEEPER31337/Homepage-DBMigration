# Not used on main project.

from pymysql import OperationalError
from typing import Tuple
from util.typedef import Table
from db_controller.db_controller import DBController


class PasswordSpliter:
    dbController: DBController

    newPasswordCol: str

    addNewPasswordColumnFormat = (
        "ALTER TABLE xe_member"
        " ADD {newPasswordCol} VARCHAR(60) DEFAULT NULL;")

    selectPasswordQuery = (
        "SELECT member_srl, password"
        " FROM xe_member;")

    updatePasswordFormat = (
        "UPDATE xe_member"
        " SET {newPasswordCol} = %({newPasswordCol})s"
        " WHERE member_srl = %(member_srl)s;"
    )

    def __init__(self, newPasswordCol: str = "new_password") -> None:
        self.newPasswordCol = newPasswordCol

    def setDBController(self, dbController: DBController) -> None:
        self.dbController = dbController

    def addNewPasswordColumn(self) -> None:
        try:
            self.dbController.getCursor().execute(self.formatAddNewPasswordColumnQuery())
        except OperationalError as oe:
            print(
                f"{oe} : There is a column already. From {self.addNewPasswordColumn.__name__}.")

    def formatAddNewPasswordColumnQuery(self) -> str:
        return self.addNewPasswordColumnFormat.format(newPasswordCol=self.newPasswordCol)

    def selectPassword(self) -> Table:
        cursor = self.dbController.getCursor()
        cursor.execute(self.selectPasswordQuery)
        passwordTable = cursor.fetchall()

        return passwordTable

    def getNewPasswordTable(self, passwordTable: Table) -> Table:
        saltHash: Tuple[str, str]

        for i, row in enumerate(passwordTable):
            saltHash = self.getSaltHash(row["password"])
            # TODO 오래된 패스워드?
            passwordTable[i][self.newPasswordCol] = saltHash[0] + \
                ':' + saltHash[1]

        return passwordTable

    def getSaltHash(self, password: str) -> Tuple[str, str]:
        salt: str
        hashStr: str

        splitedPassword = password.split(':')

        # 오래된 패스워드, 단순 해쉬로 이루어져 있음
        if(len(splitedPassword) < 4):
            salt = ""
            hashStr = splitedPassword[0]

        # 최근 로그인한 계정의 패스워드
        else:
            salt = splitedPassword[2]
            hashStr = splitedPassword[3]

        return (salt, hashStr)

    def updatePassword(self, newPasswordTable: Table) -> None:
        self.dbController.getCursor().executemany(
            self.formatUpdatePasswordQuery(), newPasswordTable)
        self.dbController.getDB().commit()

    def formatUpdatePasswordQuery(self) -> str:
        return self.updatePasswordFormat.format(newPasswordCol=self.newPasswordCol)

    def splitPassword(self) -> None:
        self.addNewPasswordColumn()
        passwordTable = self.selectPassword()
        newPasswordTable = self.getNewPasswordTable(passwordTable)
        self.updatePassword(newPasswordTable)
