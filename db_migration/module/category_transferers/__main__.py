from util.db_controller import DBController
from module.category_transferers.direct_category_transferer import DirectCategoryTransferer
from module.category_transferers.leaf_category_transferer import LeafCategoryTransferer

# TODO 숨겨진 게시판 찾기 기능 추가(깊이 3이상)


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

    directCategoryTransferer.appendCategoryTransfer(
        (4256, 117)  # 전체세미나 -> 발표자료
        , (5963, 5424)  # 스터디보고서 -> 스터디 발표자료
        , (168497, 5424)  # 2021년 겨울방학 스터디 -> 스터디 발표자료
        , (34608, 116))  # KUCIS -> 자유게시판

    directCategoryTransferer.transferCategory()


def transferSingleLeafCategory(newDB: DBController):
    singleLeafCategoryTransferer = LeafCategoryTransferer()
    singleLeafCategoryTransferer.setDBController(newDB)
    singleLeafCategoryTransferer.setLeafDepth(1)

    singleLeafCategoryTransferer.appendCategoryTransfer(
        2996  # 기술문서 하위 게시판 -> 기술문서
        , 5125  # 정보 하위 게시판 -> 정보
        , (105900, 5424)  # 2021년 2학기 스터디 하위 게시판 -> 스터디 발표자료
        , (147718, 116))  # 연재글 하위 게시판 -> 자유게시판

    singleLeafCategoryTransferer.transferCategory()


def transferDoubleLeafCategory(newDB: DBController):
    doubleLeafCategoryTransferer = LeafCategoryTransferer()
    doubleLeafCategoryTransferer.setDBController(newDB)
    doubleLeafCategoryTransferer.setLeafDepth(2)

    doubleLeafCategoryTransferer.appendCategoryTransferDict(
        5424)  # 이전 스터디 -> 스터디 발표자료

    doubleLeafCategoryTransferer.transferCategory()


if __name__ == "__main__":
    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    transferCategory(newDB)
