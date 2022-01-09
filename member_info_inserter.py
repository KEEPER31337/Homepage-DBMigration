
# Add phone/student number columns, parse extra_vars column and update rows
# If there is phone/student number column already, it doesn't work. Please drop both of them.
# Need member_info_parser.py

from pymysql import connect, cursors
from pymysql.err import OperationalError
from member_info_parser import parseExtraVars

def getDB() :
    db = connect(
        user='root', # Your mysql username
        passwd='', # Your mysql password
        host='127.0.0.1',
        db='keeper',
        charset='utf8'
    )

    return db

def getDBCursor(db) :
    return db.cursor(cursors.DictCursor)

def addColumns(cursor) :
    addPhoneNumberColumnSql = "ALTER TABLE xe_member ADD phone_number VARCHAR(45) DEFAULT NULL"

    addStudentNumberColumnSql = "ALTER TABLE xe_member ADD student_number VARCHAR(45) DEFAULT NULL"

    try :
        cursor.execute(addPhoneNumberColumnSql)
        cursor.execute(addStudentNumberColumnSql)
    
    except OperationalError as oe:
        print(f"{oe} : There is phone or student number column already! Please drop both of them.")
        return 1
    
    return 0

def getRows(cursor) :
    selectMemberSql = "SELECT member_srl, extra_vars FROM `xe_member`;"
    cursor.execute(selectMemberSql)
    result = cursor.fetchall()

    return result

def appendInfo(tableRows) :
    for i, row in enumerate(tableRows) :
        print(f"Member serial : {row['member_srl']}")
        extraVars = parseExtraVars(row['extra_vars'])
        print()
        tableRows[i].update(extraVars)
    
    return tableRows

def updateRows(cursor, data, db) :
    updateMemberSql = "UPDATE xe_member SET phone_number = %s, student_number = %s WHERE member_srl = %s;"
    # 일반 포맷과는 다르게 PyMySQL의 placeholder는 값을 전부 %s로 대치

    cursor.executemany(updateMemberSql,data)
    db.commit()


def convertDictToData(dicts) :
    data = []
    for singleDict in dicts :
        singleData = [
            singleDict['phone_number'],
            singleDict['student_number'],
            singleDict['member_srl']
        ]
        data.append(singleData)
    
    return data


if __name__ == "__main__" :
    keeper_db = getDB()
    cursor = getDBCursor(keeper_db)
    
    if (addColumns(cursor)) : exit()

    tableRows = getRows(cursor)
    tableRows = appendInfo(tableRows)

    data = convertDictToData(tableRows)

    updateRows(cursor, data, keeper_db)
