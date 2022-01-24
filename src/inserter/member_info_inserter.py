
# Add student number columns, parse extra_vars column and update rows
# If there is student number column already, it doesn't work. Please drop it.
# Need member_info_parser.py

from pymysql import connect, cursors
from pymysql.err import OperationalError
from db_controller.db_controller import DBController
from inserter.extra_vars_parser import ExtraVarsParser

class ExtraVarsInserter:
    addStudentNumberColumnQuery = "ALTER TABLE xe_member ADD student_number VARCHAR(45) DEFAULT NULL"
    selectMemberQuery = "SELECT member_srl, extra_vars FROM `xe_member`;"
    updateMemberQuery = "UPDATE xe_member SET student_number = %s WHERE member_srl = %s;"

    def addColumns(self,oldDB: DBController) :
        oldDB.getCursor().execute(self.addStudentNumberColumnQuery)

    def getMemberRows(self,oldDB: DBController) :
        cursor = oldDB.getCursor()
        cursor.execute(self.selectMemberQuery)
        return cursor.fetchall()

    def appendInfo(self,memberRows) :
        for i, row in enumerate(memberRows) :
            print(f"Member serial : {row['member_srl']}")
            parsedExtraVars = ExtraVarsParser.parseExtraVars(row['extra_vars'])
            print()
            memberRows[i].update(parsedExtraVars)
        
        return memberRows

    def updateRows(cursor, data, db) :
        cursor.executemany(updateMemberSql,data)
        db.commit()


    def convertDictToData(dicts) :
        data = []
        for singleDict in dicts :
            singleData = [
                singleDict['student_number'],
                singleDict['member_srl']
            ]
            data.append(singleData)
        
        return data

    def insertMemberInfo(cursor) :
        addColumns(cursor)
        
        tableRows = getRows(cursor)
        tableRows = appendInfo(tableRows)

        data = convertDictToData(tableRows)

        updateRows(cursor, data, keeper_db)


if __name__ == "__main__" :
    keeper_db = getDB()
    cursor = getDBCursor(keeper_db)
    
    addColumns(cursor)

    tableRows = getRows(cursor)
    tableRows = appendInfo(tableRows)

    data = convertDictToData(tableRows)

    updateRows(cursor, data, keeper_db)
