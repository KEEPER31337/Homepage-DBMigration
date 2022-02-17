from db_controller.db_controller import DBController


def migrateData(newDB: DBController) -> None:
    migratorTestSql = open("./resource/data_migrator.sql",'r')

    newDB.getCursor().execute(migratorTestSql.read())
    newDB.getDB().commit()


if __name__ == "__main__":
    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    migrateData(newDB)
