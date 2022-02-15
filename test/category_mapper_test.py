from category_mapper.category_mapper import CategoryMapper
from db_controller.db_controller import DBController

oldDB = DBController()
oldDB.setDBName("keeper_copy")
oldDB.setDB()

categoryMapper = CategoryMapper()
categoryMapper.setDBController(oldDB)

categoryMapper.mapCategory()
