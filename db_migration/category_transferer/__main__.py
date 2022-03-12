from db_controller.db_controller import DBController
from category_transferer.direct_category_transferer import DirectCategoryTransferer
from category_transferer.leaf_category_transferer import LeafCategoryTransferer


def transferCategory(newDB: DBController):
    print(f"Transfering posting category direct on {newDB.getDBName()}...")
    transferDirectCategory(newDB)

    print(
        f"Transfering posting category at single depth on {newDB.getDBName()}...")
    transferSingleLeafCategory(newDB)

    print(
        f"Transfering posting category at double depth on {newDB.getDBName()}...")
    transferDoubleLeafCategory(newDB)


def transferDirectCategory(newDB: DBController):
    directCategoryTransferer = DirectCategoryTransferer()
    directCategoryTransferer.setDBController(newDB)

    # 전체세미나 -> 발표자료
    directCategoryTransferer.appendCategoryTransferDict(4256, 117)
    # 스터디보고서 -> 스터디 발표자료
    directCategoryTransferer.appendCategoryTransferDict(5963, 5424)
    # 2021년 겨울방학 스터디 -> 스터디 발표자료
    directCategoryTransferer.appendCategoryTransferDict(168497, 5424)
    # KUCIS -> 자유게시판
    directCategoryTransferer.appendCategoryTransferDict(34608, 116)

    directCategoryTransferer.transferCategory()


def transferSingleLeafCategory(newDB: DBController):
    singleLeafCategoryTransferer = LeafCategoryTransferer()
    singleLeafCategoryTransferer.setDBController(newDB)
    singleLeafCategoryTransferer.setLeafDepth(1)

    # 기술문서 하위 게시판 -> 기술문서
    singleLeafCategoryTransferer.appendCategoryTransferDict(2996)
    # 정보 하위 게시판 -> 정보
    singleLeafCategoryTransferer.appendCategoryTransferDict(5125)
    # 2021년 2학기 스터디 하위 게시판 -> 스터디 발표자료
    singleLeafCategoryTransferer.appendCategoryTransferDict(105900, 5424)
    # 연재글 하위 게시판 -> 자유게시판
    singleLeafCategoryTransferer.appendCategoryTransferDict(147718, 116)

    singleLeafCategoryTransferer.transferCategory()


def transferDoubleLeafCategory(newDB: DBController):
    doubleLeafCategoryTransferer = LeafCategoryTransferer()
    doubleLeafCategoryTransferer.setDBController(newDB)
    doubleLeafCategoryTransferer.setLeafDepth(2)

    # 이전 스터디 -> 스터디 발표자료
    doubleLeafCategoryTransferer.appendCategoryTransferDict(5424)

    doubleLeafCategoryTransferer.transferCategory()


if __name__ == "__main__":
    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    transferCategory(newDB)
