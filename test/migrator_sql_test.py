from db_controller.db_controller import DBController


# TODO : RUN 프로젝트 구조 구상
# TODO : 가변 DB, 다중 sql 쿼리 실행방법 결정 bash or pymysql

def testMigratorSql(newDB: DBController) -> None:
    migratorTestSql = open("./migrator_test.sql")

    newDB.getCursor().execute(migratorTestSql.read())
    newDB.getDB().commit()


if __name__ == "__main__":
    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    testMigratorSql(newDB)
