from pymysql import connect, cursors
from pymysql.connections import Connection


class DBController:
    db: Connection
    user = 'root'
    passwd = ''
    host = '127.0.0.1'
    dbName = ''
    charset = 'utf8'

    def setUser(self, user: str): self.user = user
    def setDBName(self, dbName: str): self.dbName = dbName
    def setPasswd(self, passwd: str): self.passwd = passwd

    def setDB(self):
        self.db = connect(user=self.user,
                          passwd=self.passwd,
                          host=self.host,
                          db=self.dbName,
                          charset=self.charset
                          )

    def getDB(self) -> Connection: return self.db

    def getCursor(
        self) -> cursors.DictCursor: return self.db.cursor(cursors.DictCursor)

    def selectTable(self, selctQuery: str, data: list) -> list:
        cursor = self.getCursor()
        cursor.execute(selctQuery, data)
        return cursor.fetchall()

    def insertUpdateTable(self, insertUpdateQuery: str, data: list) -> None:
        cursor = self.getCursor()
        cursor.executemany(insertUpdateQuery, data)
        self.db.commit()
