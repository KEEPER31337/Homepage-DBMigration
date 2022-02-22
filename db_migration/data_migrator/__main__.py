import data_migrator
from os.path import dirname
from db_controller.db_controller import DBController


def migrateData(oldDB: DBController, newDB: DBController) -> None:
    print(f"Migrating general data to {newDB.getDBName()}...")

    modulePath = dirname(data_migrator.__file__)
    sqlFilePath = "resource/data_migrator.sql"
    dataMigratorSql = open(modulePath + "/" + sqlFilePath, 'r')
    dataMigratorSqlQuery = dataMigratorSql.read().format(
        srcDB=oldDB.getDBName(),
        dstDB=newDB.getDBName())

    newDB.getCursor().execute(dataMigratorSqlQuery)
    newDB.getDB().commit()


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")

    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    migrateData(oldDB, newDB)
