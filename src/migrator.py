from src.db_controller.db_controller import DBController
from src.seperator.job_seperator import JobSeperator


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper")
    oldDB.setDB()

    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    jobSeperator = JobSeperator()

    jobSeperator.addGroupSrl("회장",34603,1)
    jobSeperator.addGroupSrl("부회장",53180,2)
    jobSeperator.addGroupSrl("대외부장",34131,3)
    jobSeperator.addGroupSrl("학술부장",34599,4)
    jobSeperator.addGroupSrl("전산관리자",34600,5)
    jobSeperator.addGroupSrl("서기",34601,6)
    jobSeperator.addGroupSrl("총무",34602,7)
    jobSeperator.addGroupSrl("사서",75521,8)

    jobSeperator.selectGroupTable(oldDB)
    jobSeperator.insertJobTable(newDB)
    


