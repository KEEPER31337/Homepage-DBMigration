from db_controllers.db_controller import DBController
from module.extra_vars_inserters.extra_vars_inserter import ExtraVarsInserter


def insertExtraVars(oldDB: DBController) -> None:
    print(f"Inserting parsed extra vars on {oldDB.getDBName()}...")

    extraVarsInserter = ExtraVarsInserter()
    extraVarsInserter.setDBController(oldDB)
    extraVarsInserter.insertExtraVars()


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")
    oldDB.setDB()

    insertExtraVars(oldDB)
