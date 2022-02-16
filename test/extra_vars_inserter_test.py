from db_controller.db_controller import DBController
from extra_vars_inserter.extra_vars_inserter import ExtraVarsInserter


def testExtraVarsInserter(oldDB: DBController) -> None:
    extraVarsInserter = ExtraVarsInserter()
    extraVarsInserter.setDBController(oldDB)
    extraVarsInserter.insertExtraVars()


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")
    oldDB.setDB()

    testExtraVarsInserter(oldDB)
