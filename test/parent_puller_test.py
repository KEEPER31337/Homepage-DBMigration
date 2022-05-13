from util.db_controller import DBController
from module.parent_pullers.parent_puller import ParentPuller
from pprint import pprint as pp

oldDB = DBController()
oldDB.setDBName("keeper_copy")
oldDB.setDB()

parentPuller = ParentPuller()
parentPuller.setDBController(oldDB)

testComments = [{'comment_srl': 1, 'parent_srl': 0},
                {'comment_srl': 2, 'parent_srl': 1},
                {'comment_srl': 3, 'parent_srl': 2},
                {'comment_srl': 4, 'parent_srl': 3},
                {'comment_srl': 5, 'parent_srl': 4},
                {'comment_srl': 6, 'parent_srl': 5},
                {'comment_srl': 7, 'parent_srl': 6},
                {'comment_srl': 8, 'parent_srl': 2},
                {'comment_srl': 9, 'parent_srl': 3},
                {'comment_srl': 10, 'parent_srl': 0},
                {'comment_srl': 11, 'parent_srl': 8},
                {'comment_srl': 12, 'parent_srl': 13},
                {'comment_srl': 13, 'parent_srl': 13},
                {'comment_srl': 14, 'parent_srl': 15}]

parentPuller.__parentPulledTable = testComments
parentPuller.__initVisited()
pp(parentPuller.__travelParentPulledTable())

# parentPuller.pullParent()
