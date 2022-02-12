
from db_controller.db_controller import DBController
from library_migrator.book_migrator import BookMigrator
from library_migrator.equipment_migrator import EquipmentMigrator

bookDB = DBController()
bookDB.setDBName("Library2")
bookDB.setDB()

equipmentDB = DBController()
equipmentDB.setDBName("Library")
equipmentDB.setDB()

newDB = DBController()
newDB.setDBName("keeper_new")
newDB.setDB()

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

equipmentMigrator = EquipmentMigrator()
equipmentMigrator.setOldDBController(equipmentDB)
equipmentMigrator.setNewDBController(newDB)

equipmentMigrator.migrateEquipment()
