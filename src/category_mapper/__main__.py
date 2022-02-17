from category_mapper.category_mapper import CategoryMapper
from db_controller.db_controller import DBController


def mapCategory(oldDB: DBController) -> None:
    categoryMapper = CategoryMapper()
    categoryMapper.setDBController(oldDB)
    categoryMapper.mapCategory()


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")
    oldDB.setDB()

    mapCategory(oldDB)
