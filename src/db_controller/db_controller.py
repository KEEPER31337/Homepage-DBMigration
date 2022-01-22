from pymysql import connect, cursors
from pymysql.connections import Connection

class DBController :
    db = ""
    user = 'root'
    passwd = ''
    host = '127.0.0.1'
    dbName = ''
    charset='utf8'
    
    def setUser(self, user: str) : self.user = user
    def setDBName(self, dbName: str) : self.dbName = dbName
    def setPasswd(self, passwd: str) : self.passwd = passwd

    def setDB(self) :
        self.db = connect(user=self.user,
        passwd=self.passwd,
        host=self.host,
        db=self.dbName,
        charset=self.charset
    )

    def getDB(self) -> Connection : return self.db

    def getCursor(self) -> cursors.DictCursor : return self.db.cursor(cursors.DictCursor)

