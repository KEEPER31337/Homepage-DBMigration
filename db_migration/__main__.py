from category_transferer.__main__ import transferCategory
from db_controller.db_controller import DBController
from category_mapper.__main__ import mapCategory
from category_controller.__main__ import controlCategory
from extra_vars_inserter.__main__ import insertExtraVars
from html_content_cleaner.__main__ import cleanHtmlContent
from parent_puller.__main__ import pullParent
from data_migrator.__main__ import migrateData
from group_seperator.__main__ import seperateGroup
from library_migrator.__main__ import migrateLibrary


if __name__ == "__main__":
    passwd = ""
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")
    oldDB.setPasswd(passwd)
    oldDB.setDB()

    bookDB = DBController()
    bookDB.setDBName("Library2")
    bookDB.setPasswd(passwd)
    bookDB.setDB()

    equipmentDB = DBController()
    equipmentDB.setDBName("Library")
    equipmentDB.setPasswd(passwd)
    equipmentDB.setDB()

    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setPasswd(passwd)
    newDB.setDB()

    insertExtraVars(oldDB)
    cleanHtmlContent(oldDB)
    mapCategory(oldDB)
    pullParent(oldDB)

    migrateData(oldDB, newDB)

    seperateGroup(oldDB, newDB)
    migrateLibrary(bookDB, equipmentDB, newDB)
    controlCategory(newDB)
    transferCategory(newDB)

    print("DBMigration complete.")
