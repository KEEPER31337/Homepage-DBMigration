from group_seperator.type_rank_seperator import TypeRankSeperator


class RankSeperator(TypeRankSeperator):

    typeRankIdCol = "member_rank_id"

    def seperateRank(self) -> None:
        self.updateTypeRankTable()
