from src.db_controller.db_controller import DBController
from seperator.job_seperator import JobSeperator


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper")
    oldDB.setDB()

    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    jobSeperator = JobSeperator()

    jobSeperator.addJobSrl("회장",34603,1)
    jobSeperator.addJobSrl("부회장",53180,2)
    jobSeperator.addJobSrl("대외부장",34131,3)
    jobSeperator.addJobSrl("학술부장",34599,4)
    jobSeperator.addJobSrl("전산관리자",34600,5)
    jobSeperator.addJobSrl("서기",34601,6)
    jobSeperator.addJobSrl("총무",34602,7)
    jobSeperator.addJobSrl("사서",75521,8)

    jobSeperator.setJobMemberTable(oldDB)
    jobSeperator.insertJobMemberTable(newDB)
    


