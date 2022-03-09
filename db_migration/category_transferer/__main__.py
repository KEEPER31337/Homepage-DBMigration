from category_transferer.direct_category_transferer import DirectCategoryTransferer
from category_transferer.leaf_category_transferer import LeafCategoryTransferer
from db_controller.db_controller import DBController


def transferCategory(newDB: DBController):
    transferDirectCategory(newDB)
    transferLeafCategory(newDB)

def transferDirectCategory(newDB: DBController):
    directCategoryTransferer = DirectCategoryTransferer()
    directCategoryTransferer.setDBController(newDB)

    # append

    directCategoryTransferer.transferCategory()

def transferLeafCategory(newDB: DBController):
    leafCategoryTransferer = LeafCategoryTransferer()
    leafCategoryTransferer.setDBController(newDB)

    # append
    # TODO: 1단 / 2단 분리
    leafCategoryTransferer.transferCategory()

if __name__ == "__main__":
    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    transferCategory(newDB)