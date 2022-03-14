from group_seperators.type_rank_seperator import TypeRankSeperator


class TypeSeperator(TypeRankSeperator):

    def __init__(self,
                 memberSrlCol: str = "member_id",
                 groupSrlCol: str = "member_type_id",
                 groupTitleCol: str = "type_name",
                 typeIdCol: str = "member_type_id") -> None:

        super().__init__(memberSrlCol, groupSrlCol, groupTitleCol, typeIdCol)

    def seperateType(self) -> None:
        self.seperateTypeRank()
