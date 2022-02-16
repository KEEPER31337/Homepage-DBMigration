from db_controller.db_controller import DBController


def testMigratorSql(newDB: DBController) -> None:
    migratorTestSql = open("./migrator_test.sql")

    newDB.getCursor().execute(migratorTestSql.read())
    newDB.getDB().commit()


if __name__ == "__main__":
    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    testMigratorSql(newDB)
