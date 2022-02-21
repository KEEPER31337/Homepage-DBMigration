
from db_controller.db_controller import DBController
from category_controller.category_controller import CategoryController


def controlCategory(newDB: DBController):
    categoryList = [
    (219, 'KEEPER', None, None),
    (29422, '동아리 소개', 219, 'about'),
    (105, '공지사항', 2, 'board'),
    (6105, '건의사항', 2, 'board'),
    (116, '자유게시판', 2, 'board'),
    (147718, '연재글', 2, 'board'),
    (117, '발표자료', 3, 'board'),
    (105900, '스터디', 3, 'board'),
    (2996, '기술문서', 3, 'board'),
    (23400, '회계부', 3, 'board'),
    (34608, 'KUCIS', 3, 'board'),
    (5125, '정보', None, None),
    (508, '해킹대회정보', 5125, 'board'),
    (648, '유용한사이트', 5125, 'board'),
    (647, 'Tools', 5125, 'board'),
    (662, '외부문서&강의', 5125, 'board'),
    (81570, '취업&면접', 5125, 'board'),
    (1377, '시험', 5125, 'board'),
    (106402, '도서 신청', 5, 'library'),
    (60024, '도서 대여', 5, 'library'),
    (84493, '기자재 대여', 5, 'library'),
    (30052, '랭킹', 6, 'attendance'),
    (33777, '출석부', 6, 'attendance'),
    (11302, '게임', 6, 'game')]

    newCategoryList = [
    (8, '이벤트', 219, 'event'),
    (9, '동아리 일정', 219, 'schedule'), 
    (2, '게시판', None, None),
    (3, '동아리활동', None, None),
    (5, '서비스', None, None),   
    (27, '기자재 신청', 5, 'library'),
    (6, '포인트', None, None)
]
    
    categoryController = CategoryController()
    categoryController.setDBController(newDB)
    categoryController.appendCategoryByList(categoryList,categoryController.categoryTable)
    categoryController.appendCategoryByList(newCategoryList,categoryController.newCategoryTable)
    categoryController.controlCategory()


if __name__ == "__main__":
    newDB = DBController()
    newDB.setDBName("keeper_new")
    newDB.setDB()

    controlCategory(newDB)
