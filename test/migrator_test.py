from db_controller.db_controller import DBController
from extra_vars_extractor.extra_vars_inserter import ExtraVarsInserter
from group_seperator.job_seperator import JobSeperator
from group_seperator.rank_seperator import RankSeperator
from group_seperator.type_seperator import TypeSeperator


if __name__ == "__main__":
    oldDB = DBController()
#     oldDB.setDBName("keeper")
#     oldDB.setDB()

#     newDB = DBController()
#     newDB.setDBName("keeper_new")
#     newDB.setDB()

#     # --------------------------------------

#     extraVarsInserter = ExtraVarsInserter()
#     extraVarsInserter.setDBController(oldDB)
#     # extraVarsInserter.insertExtraVars()

#     # --------------------------------------

#     jobSeperator = JobSeperator()
#     jobSeperator.setOldDBController(oldDB)
#     jobSeperator.setNewDBController(newDB)

#     jobSeperator.addGroupSrl("회장", 34603, 1)
#     jobSeperator.addGroupSrl("부회장", 53180, 2)
#     jobSeperator.addGroupSrl("대외부장", 34131, 3)
#     jobSeperator.addGroupSrl("학술부장", 34599, 4)
#     jobSeperator.addGroupSrl("전산관리자", 34600, 5)
#     jobSeperator.addGroupSrl("서기", 34601, 6)
#     jobSeperator.addGroupSrl("총무", 34602, 7)
#     jobSeperator.addGroupSrl("사서", 75521, 8)
#     jobSeperator.setDefaultJobId(9)

#     jobSeperator.seperateJob()

#     # --------------------------------------

#     typeSeperator = TypeSeperator()
#     typeSeperator.setOldDBController(oldDB)
#     typeSeperator.setNewDBController(newDB)

#     typeSeperator.addGroupSrl("비회원", 1, 1)
#     typeSeperator.addGroupSrl("정회원", 2, 2)
#     typeSeperator.addGroupSrl("휴면회원", 3, 3)
#     typeSeperator.addGroupSrl("졸업", 6236, 4)
#     typeSeperator.addGroupSrl("탈퇴", 51938, 5)

#     typeSeperator.seperateTypeRank()

#     # --------------------------------------

#     rankSeperator = RankSeperator()
#     rankSeperator.setOldDBController(oldDB)
#     rankSeperator.setNewDBController(newDB)

#     rankSeperator.addGroupSrl("신입회원", 21359, 1)
#     rankSeperator.addGroupSrl("우수회원", 28004, 2)
#     rankSeperator.addGroupSrl("특별회원", 52603, 3)

#     rankSeperator.seperateTypeRank()
