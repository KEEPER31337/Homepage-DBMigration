from module.category_mappers.category_mapper import CategoryMapper
from util.db_controller import DBController


def mapCategory(oldDB: DBController) -> None:
    print(f"Mapping posting category on {oldDB.getDBName()}...")

    categoryMapper = CategoryMapper()
    categoryMapper.setDBController(oldDB)
    categoryMapper.mapCategory()


if __name__ == "__main__":
    oldDB = DBController()
    oldDB.setDBName("keeper_copy")
    oldDB.setDB()

    mapCategory(oldDB)
