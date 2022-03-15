from module.group_seperators.type_rank_seperator import TypeRankSeperator


class RankSeperator(TypeRankSeperator):

    def __init__(self,
                 memberSrlCol: str = "member_id",
                 groupSrlCol: str = "member_rank_id",
                 groupTitleCol: str = "rank_name",
                 rankIdCol: str = "member_rank_id") -> None:

        super().__init__(memberSrlCol, groupSrlCol, groupTitleCol, rankIdCol)

    def seperateRank(self) -> None:
        self.seperateTypeRank()
