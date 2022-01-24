
# Add student number columns, parse extra_vars column and update rows
# If there is student number column already, it doesn't work. Please drop it.
# Need member_info_parser.py

from pymysql import connect, cursors
from pymysql.err import OperationalError
from inserter.extra_vars_parser import parseExtraVars

class ExtraVarsInserter:
    addStudentNumberColumnSql = "ALTER TABLE xe_member ADD student_number VARCHAR(45) DEFAULT NULL"
    def addColumns(cursor) :
        cursor.execute(addStudentNumberColumnSql)

    def getRows(cursor) :
        selectMemberSql = "SELECT member_srl, extra_vars FROM `xe_member`;"
        cursor.execute(selectMemberSql)
        return cursor.fetchall()

    def appendInfo(tableRows) :
        for i, row in enumerate(tableRows) :
            print(f"Member serial : {row['member_srl']}")
            extraVars = parseExtraVars(row['extra_vars'])
            print()
            tableRows[i].update(extraVars)
        
        return tableRows

    def updateRows(cursor, data, db) :
        updateMemberSql = "UPDATE xe_member SET student_number = %s WHERE member_srl = %s;"
        # 일반 포맷과는 다르게 PyMySQL의 placeholder는 값을 전부 %s로 대치

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
    
    if (addColumns(cursor)) : exit() # 이미 학번 column이 존재할때

    tableRows = getRows(cursor)
    tableRows = appendInfo(tableRows)

    data = convertDictToData(tableRows)

    updateRows(cursor, data, keeper_db)
