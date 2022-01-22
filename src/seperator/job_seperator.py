
class JobSeperator :
    oldJobSrlDict = {}
    oldJobSrlDictReversed = {}
    newJobSrlDict = {}

    selectJobMemberSrlSql = ("SELECT t1.member_srl AS member_id, t2.group_srl AS member_job_id"
    " FROM xe_member_group_member as t1, xe_member_group as t2" 
    " WHERE (t1.group_srl = t2.group_srl AND"
    " t1.group_srl IN("
    )

    oldJobMemberTable = []
    newJobMemberTable = []

    insertJobMemberTableSql = "INSERT INTO test VALUES(%(member_id)s,%(member_job_id)s)"


    def addJobSrl(self,jobName,oldSrl,newSrl) :
        self.oldJobSrlDict[jobName] = oldSrl
        self.oldJobSrlDictReversed[oldSrl] = jobName
        self.newJobSrlDict[jobName] = newSrl

    def getSelectJobMemberSrlSql(self) :
        conditionFormat = "%s"
        for i in range(len(self.oldJobSrlDict)-1) : conditionFormat += ",%s"
        conditionFormat += "));"

        return self.selectJobMemberSrlSql + conditionFormat

    def getOldSrlData(self) : return tuple(self.oldJobSrlDict.values())

    def getNewSrlData(self) : return tuple(self.newJobSrlDict.values())

    def setJobMemberTable(self,oldDB) :
        cursor = oldDB.getCursor()
        cursor.execute(
            self.getSelectJobMemberSrlSql(),
            self.getOldSrlData()
        )
        
        self.oldJobMemberTable = cursor.fetchall()

    def updateJobMemberTable(self) :
        tmp = self.oldJobMemberTable
        
        for i,d in enumerate(tmp) :
            job = self.oldJobSrlDictReversed[d["member_job_id"]]
            tmp[i]["member_job_id"] = self.newJobSrlDict[job]
        
        self.newJobMemberTable = tmp

    def insertJobMemberTable(self,newDB) :
        self.updateJobMemberTable()
        cursor = newDB.getCursor()
        cursor.executemany(
            self.insertJobMemberTableSql,
            self.newJobMemberTable
        )
        newDB.getDB().commit()