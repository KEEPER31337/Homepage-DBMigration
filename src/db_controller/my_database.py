from pymysql import connect, cursors

from seperator.job_seperator import JobSeperator

class DBController :
    db = ""
    user = 'root'
    passwd = ''
    host = '127.0.0.1'
    dbName = ''
    charset='utf8'

    jobSperator = ""
    
    def setUser(self,user) : self.user = user
    def setDBName(self,dbName) : self.dbName = dbName
    def setPasswd(self,passwd) : self.passwd = passwd

    def setDB(self) :
        self.db = connect(user=self.user,
        passwd=self.passwd,
        host=self.host,
        db=self.dbName,
        charset=self.charset
    )

    def getDB(self) : return self.db

    def getCursor(self) :
        return self.db.cursor(cursors.DictCursor)

