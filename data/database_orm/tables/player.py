from .. import bot_declarative_base
from utils.enums import Tier, Division, RankedQueue, Server
from sqlalchemy import Column, String, Enum, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Player(bot_declarative_base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
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
    mini_series_id = Column(Integer, ForeignKey("mini_series.id", ondelete="cascade"))
    mini_series = relationship("MiniSeries", backref="player")


class MiniSeries(bot_declarative_base):
    __tablename__ = "miniseries"

    id = Column(Integer, primary_key=True)
    target = Column(Integer)
    wins = Column(Integer)
    losses = Column(Integer)
    progress = Column(String(5))
