from group_seperator.type_rank_seperator import TypeRankSeperator


class TypeSeperator(TypeRankSeperator):

    typeRankIdCol = "member_type_id"

    def seperateType(self) -> None:
        self.updateTypeRankTable()
