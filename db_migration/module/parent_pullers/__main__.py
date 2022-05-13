from util.db_controller import DBController
from module.parent_pullers.parent_puller import ParentPuller


def pullParent(oldDB: DBController):
    print(f"Pulling up comment parent srl on {oldDB.getDBName()}...")
    parentPuller = ParentPuller()
    parentPuller.setDBController(oldDB)
    parentPuller.pullParent()


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")
    oldDB.setDB()

    pullParent(oldDB)
