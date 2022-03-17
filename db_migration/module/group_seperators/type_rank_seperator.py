from abc import ABCMeta
from util.typedef import Table
from module.group_seperators.group_seperator import GroupSeperator


class TypeRankSeperator(GroupSeperator, metaclass=ABCMeta):

    __typeRankIdCol: str

    __updateTypeRankFormat = (
        "UPDATE member"
        " SET {typeRankIdCol} = %({groupSrlCol})s"
        " WHERE id = %({memberSrlCol})s;")

    def __init__(self,
                 memberSrlCol: str,
                 groupSrlCol: str,
                 groupTitleCol: str,
                 typeRankIdCol: str) -> None:

        self.__typeRankIdCol = typeRankIdCol

        super().__init__(memberSrlCol, groupSrlCol, groupTitleCol)

    def _seperateTypeRank(self) -> None:
        typeRankSrlTable = self.__selectTypeRankSrl()
        editedTypeRankSrlTable = self.__getEditedTypeRankSrlTable(
            typeRankSrlTable)
        self.__updateTypeRank(editedTypeRankSrlTable)

    def __selectTypeRankSrl(self) -> Table:
        return self._selectGroupSrl()

    def __getEditedTypeRankSrlTable(self, typeRankSrlTable: Table) -> Table:
        return self._getEditedGroupSrlTable(typeRankSrlTable)

    def __updateTypeRank(self, typeRankSrlTable: Table) -> None:
        cursor = self._newDBController.getCursor()
        cursor.executemany(
            self.__formatUpdateTypeRankQuery(),
            typeRankSrlTable)
        # pymysql.err.IntegrityError : FK 비일치
        self._newDBController.getDB().commit()

    def __formatUpdateTypeRankQuery(self) -> str:
        return self.__updateTypeRankFormat.format(
            typeRankIdCol=self.__typeRankIdCol,
            memberSrlCol=self._memberSrlCol,
            groupSrlCol=self._groupSrlCol)
