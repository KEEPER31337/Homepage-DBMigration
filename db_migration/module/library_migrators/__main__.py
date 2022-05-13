from util.db_controller import DBController
from module.library_migrators.book_migrator import BookMigrator
from module.library_migrators.equipment_migrator import EquipmentMigrator


def migrateLibrary(bookDB: DBController, equipmentDB: DBController, newDB: DBController) -> None:
    print(
        f"Migrating book data from {bookDB.getDBName()} to {newDB.getDBName()}...")
    migrateBook(bookDB, newDB)

    print(
        f"Migrating equipment data from {equipmentDB.getDBName()} to {newDB.getDBName()}...")
    migrateEquipment(equipmentDB, newDB)


def migrateBook(bookDB: DBController, newDB: DBController) -> None:
    bookMigrator = BookMigrator()
    bookMigrator.setOldDBController(bookDB)
    bookMigrator.setNewDBController(newDB)

    bookMigrator.addBookDepartment(0, 1)
    bookMigrator.addBookDepartment(1, 2)
    bookMigrator.addBookDepartment(2, 3)
    bookMigrator.addBookDepartment(3, 4)
    bookMigrator.addBookDepartment(4, 5)
    bookMigrator.addBookDepartment(9, 6)

    bookMigrator.migrateBook()


def migrateEquipment(equipmentDB: DBController, newDB: DBController) -> None:

    equipmentMigrator = EquipmentMigrator()
    equipmentMigrator.setOldDBController(equipmentDB)
    equipmentMigrator.setNewDBController(newDB)

    equipmentMigrator.migrateEquipment()


if __name__ == "__main__":
    bookDB = DBController()
    bookDB.setDBName("Library2")
    bookDB.setDB()

    equipmentDB = DBController()
    equipmentDB.setDBName("Library")
    equipmentDB.setDB()

    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    migrateLibrary(bookDB, equipmentDB, newDB)
