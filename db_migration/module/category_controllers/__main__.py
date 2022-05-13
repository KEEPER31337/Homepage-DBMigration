
from util.db_controller import DBController
from module.category_controllers.category_controller import CategoryController


def controlCategory(newDB: DBController):
    print(f"Controlling posting categories on {newDB.getDBName()}...")


    categoryController = CategoryController()
    categoryController.setDBController(newDB)

    categoryController.appendCategory(
        # categories to insert
        (219, 'KEEPER', 0, None),
        (29422, '동아리 소개', 219, 'about'),
        (105, '공지사항', 2, 'board'),
        (6105, '건의사항', 2, 'board'),
        (116, '자유게시판', 2, 'board'),
        (63908, '익명게시판', 2, 'board'),
        (117, '발표자료', 3, 'board'),
        (105900, '2021학년도 2학기', 3, 'board'),
        (5424, '스터디 발표자료', 3, 'board'),
        (2996, '기술문서', 3, 'board'),
        (23400, '회계부', 3, 'board'),
        (5125, '정보', 4, None),
        (508, '해킹대회정보', 5125, 'board'),
        (648, '유용한사이트', 5125, 'board'),
        (647, 'Tools', 5125, 'board'),
        (662, '외부문서&강의', 5125, 'board'),
        (81570, '취업&면접', 5125, 'board'),
        (1377, '시험', 4, 'board'),
        (106402, '도서 신청', 5, 'library'),
        (60024, '도서 대여', 5, 'library'),
        (84493, '기자재 대여', 5, 'library'),
        (30052, '랭킹', 6, 'attendance'),
        (33777, '출석부', 6, 'attendance'),
        (11302, '게임', 6, 'game'),
        # categories to update
        (2, '게시판', 0, None),
        (3, '동아리활동', 0, None),
        (4, '정보', 0, None),
        (5, '서비스', 0, None),
        (6, '포인트', 0, None),
        (8, '이벤트', 219, 'event'),
        (9, '동아리 일정', 219, 'schedule'),
        (27, '기자재 신청', 5, 'library'))

    categoryController.controlCategory()


if __name__ == "__main__":
    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    controlCategory(newDB)
