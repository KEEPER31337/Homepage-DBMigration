from pymysql import connect, cursors
from pymysql.connections import Connection
from pymysql.constants import CLIENT


class DBController:
    db: Connection
    user = 'root'
    passwd = ''
    host = '127.0.0.1'
    dbName = ''
    charset = 'utf8'
    clientFlag = CLIENT.MULTI_STATEMENTS

    def setUser(self, user: str): self.user = user
    def setDBName(self, dbName: str): self.dbName = dbName
    def setPasswd(self, passwd: str): self.passwd = passwd
    def setHost(self, host: str): self.host = host

    def setDB(self):
        self.db = connect(user=self.user,
                          passwd=self.passwd,
                          host=self.host,
                          db=self.dbName,
                          charset=self.charset,
                          client_flag=self.clientFlag)

    def getDB(self) -> Connection: return self.db

    def getCursor(self) -> cursors.DictCursor:
        return self.db.cursor(cursors.DictCursor)

    def getDBName(self) -> Connection: return self.dbName

    def selectTable(self, selectQuery: str, data: list) -> list:
        cursor = self.getCursor()
        cursor.execute(selectQuery, data)
        return cursor.fetchall()

    def insertUpdateTable(self, insertUpdateQuery: str, data: list) -> None:
        cursor = self.getCursor()
        cursor.executemany(insertUpdateQuery, data)
        self.db.commit()
