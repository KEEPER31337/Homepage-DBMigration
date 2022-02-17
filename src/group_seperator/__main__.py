from db_controller.db_controller import DBController
from group_seperator.job_seperator import JobSeperator
from group_seperator.rank_seperator import RankSeperator
from group_seperator.type_seperator import TypeSeperator


def seperateGroup(oldDB: DBController, newDB: DBController) -> None:

    seperateJob(oldDB, newDB)
    seperateType(oldDB, newDB)
    seperateRank(oldDB, newDB)


def seperateJob(oldDB: DBController, newDB: DBController) -> None:

    jobSeperator = JobSeperator()
    jobSeperator.setOldDBController(oldDB)
    jobSeperator.setNewDBController(newDB)

    jobSeperator.addGroupSrlDict("회장", 34603, 1)
    jobSeperator.addGroupSrlDict("부회장", 53180, 2)
    jobSeperator.addGroupSrlDict("대외부장", 34131, 3)
    jobSeperator.addGroupSrlDict("학술부장", 34599, 4)
    jobSeperator.addGroupSrlDict("전산관리자", 34600, 5)
    jobSeperator.addGroupSrlDict("서기", 34601, 6)
    jobSeperator.addGroupSrlDict("총무", 34602, 7)
    jobSeperator.addGroupSrlDict("사서", 75521, 8)
    jobSeperator.setDefaultJobId(9)

    jobSeperator.seperateJob()


def seperateType(oldDB: DBController, newDB: DBController) -> None:

    typeSeperator = TypeSeperator()
    typeSeperator.setOldDBController(oldDB)
    typeSeperator.setNewDBController(newDB)

    typeSeperator.addGroupSrlDict("비회원", 1, 1)
    typeSeperator.addGroupSrlDict("정회원", 2, 2)
    typeSeperator.addGroupSrlDict("휴면회원", 3, 3)
    typeSeperator.addGroupSrlDict("졸업", 6236, 4)
    typeSeperator.addGroupSrlDict("탈퇴", 51938, 5)

    typeSeperator.seperateTypeRank()


def seperateRank(oldDB: DBController, newDB: DBController) -> None:

    rankSeperator = RankSeperator()
    rankSeperator.setOldDBController(oldDB)
    rankSeperator.setNewDBController(newDB)

    rankSeperator.addGroupSrlDict("신입회원", 21359, 1)
    rankSeperator.addGroupSrlDict("우수회원", 28004, 2)
    rankSeperator.addGroupSrlDict("특별회원", 52603, 3)

    rankSeperator.seperateTypeRank()


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper")
    oldDB.setDB()

    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    seperateGroup(oldDB, newDB)
