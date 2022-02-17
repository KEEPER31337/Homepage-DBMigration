from db_controller.db_controller import DBController


# TODO : RUN 프로젝트 구조 구상

def testMigratorSql(newDB: DBController) -> None:
    migratorTestSql = open("./migrator_test.sql")

    newDB.getCursor().execute(migratorTestSql.read())
    newDB.getDB().commit()


if __name__ == "__main__":
    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    testMigratorSql(newDB)
