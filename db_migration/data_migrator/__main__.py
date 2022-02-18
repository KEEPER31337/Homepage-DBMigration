import data_migrator
from os.path import dirname
from db_controller.db_controller import DBController


def migrateData(newDB: DBController) -> None:
    print(f"Migrating general data to {newDB.getDBName()}...")

    modulePath = dirname(data_migrator.__file__)
    sqlFilePath = "resource/data_migrator.sql"
    migratorTestSql = open(modulePath + "/" + sqlFilePath, 'r')

    newDB.getCursor().execute(migratorTestSql.read())
    newDB.getDB().commit()


if __name__ == "__main__":
    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    migrateData(newDB)
