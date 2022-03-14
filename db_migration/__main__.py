from category_transferers.__main__ import transferCategory
from db_controllers.db_controller import DBController
from category_mappers.__main__ import mapCategory
from category_controllers.__main__ import controlCategory
from extra_vars_inserters.__main__ import insertExtraVars
from html_content_cleaners.__main__ import cleanHtmlContent
from parent_pullers.__main__ import pullParent
from data_migrators.__main__ import migrateData
from group_seperators.__main__ import seperateGroup
from library_migrators.__main__ import migrateLibrary


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
