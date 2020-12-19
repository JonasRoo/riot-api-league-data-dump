from typing import Mapping, Any, Tuple
from sqlalchemy import Column, String, Enum, Integer, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, class_mapper
from .. import bot_declarative_base
from utils.enums import Tier, Division, RankedQueue, Server
from collections import namedtuple

EnumFieldMap = namedtuple("EnumFieldMap", ("leagueEntryDTOName", "alias", "enum"))

_ENUM_FIELDS = [
    EnumFieldMap(leagueEntryDTOName="queueType", alias="ranked_queue", enum=RankedQueue),
    EnumFieldMap(leagueEntryDTOName="tier", alias="tier", enum=Tier),
    EnumFieldMap(leagueEntryDTOName="rank", alias="division", enum=Division),
]


class Player(bot_declarative_base):
    """
    A player represents a member of a RankedQueue with given ranked information.
    """

    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    league_id = Column(String)
    # ENUMS
    server = Column(Enum(Server))
    ranked_queue = Column(Enum(RankedQueue))
    tier = Column(Enum(Tier))
    division = Column(Enum(Division))
    # Return fields
    summoner_id = Column(String)
    summoner_name = Column(String)
    league_points = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    is_veteran = Column(Boolean)
    is_inactive = Column(Boolean)
    is_fresh_blood = Column(Boolean)
    is_hot_streak = Column(Boolean)
    mini_series_id = Column(Integer, ForeignKey("miniseries.id", ondelete="cascade"), nullable=True)
    mini_series = relationship("MiniSeries", backref="player")

    # There can only be one entry for a summoner on a server in a given queue
    __table_args__ = (
        UniqueConstraint(
            "server", "summoner_id", "ranked_queue", name="_one_entry_per_server_queue_uc"
        ),
    )

    @classmethod
    def _api_model_map(cls) -> Mapping[str, str]:
        """
        Produces an internal mapping of named fields from the API response to named fields of this table.
        Format:
            {
                "key_in_api_response_body": "table_field_name"
            }

        Returns:
            Mapping[str, str]: mapping of API response fields to table fields.
        """
        return {
            "leagueId": "league_id",
            "summonerId": "summoner_id",
            "summonerName": "summoner_name",
            "leaguePoints": "league_points",
            "veteran": "is_veteran",
            "inactive": "is_inactive",
            "freshBlood": "is_fresh_blood",
            "hotStreak": "is_hot_streak",
        }

    @classmethod
    def _from_api_dict(cls, league_entry_DTO: Mapping[str, Any]) -> "Player":
        """
        Instantiates a `Player` object from a list-member(!)
        of the raw response of the Riot API `GET getLeagueEntries` endpoint.

        Returns:
            Player: The generated `Player` instance.
        """
        new_instance = {}
        mapper = cls._api_model_map()
        for k, v in mapper.items():
            new_instance[v] = league_entry_DTO.pop(k)
        for field in _ENUM_FIELDS:
            new_instance[field.alias] = field.enum(league_entry_DTO.pop(field.leagueEntryDTOName))

        return cls(**new_instance)


class MiniSeries(bot_declarative_base):
    """
    A miniseries represents a promotional series within a ranked queue.
    """

    __tablename__ = "miniseries"

    id = Column(Integer, primary_key=True)
    target = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    # looks like this "xo-", "xxo--"
    # 2 possible lengths: a) 5 - between divisions, b) 3 - between tiers within a division
    progress = Column(String(5))
