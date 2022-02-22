from db_controller.db_controller import DBController
from parent_puller.parent_puller import ParentPuller


def pullParent(oldDB: DBController):
    parentPuller = ParentPuller()
    parentPuller.setDBController(oldDB)
    parentPuller.pullParent()


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")
    oldDB.setDB()

    pullParent(oldDB)
