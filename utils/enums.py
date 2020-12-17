import enum


class Server(enum.Enum):
    """
    Represents a playable League of Legends server.
    > Enum member names: based on common naming conventions within the community,
    > Member values: mapped to routing values within the Riot LoL API.
    """

    BR = "BR1"
    EUNE = "EUN1"
    EUW = "EUW1"
    JP = "JP1"
    KR = "KR"
    LAN = "LA1"
    LAS = "LA2"
    NA = "NA1"
    OCE = "OC1"
    RU = "RU"
    TR = "TR1"


class RankedQueue(enum.Enum):
    """
    Represents a playable (competitive) League of Legends queue that players can be ranked in.
    > Enum member values are mapped to queriable endpoint values for the Riot LoL API.
    """

    SOLO_DUO = "RANKED_SOLO_5x5"
    FLEX_SR = "RANKED_FLEX_SR"
    FLEX_TT = "RANKED_FLEX_TT"


class Tier(enum.Enum):
    """
    Represents a (`GET leagueEntries`-queryable!) competitive tier a player can be in.
    Challenger, Grandmaster and Masters need to be fetched from a separate endpoint!
    """

    # CHALLENGER = "CHALLENGER"
    # GRANDMASTER = "GRANDMASTER"
    # MASTER = "MASTER"
    DIAMOND = "DIAMOND"
    PLATINUM = "PLATINUM"
    GOLD = "GOLD"
    SILVER = "SILVER"
    BRONZE = "BRONZE"
    IRON = "IRON"


class Division(enum.Enum):
    """
    Represents a division (within a tier) a player can be in.
    Each division has 4 tiers (the lower the number, the higher the rank) - except for Master, Grandmastera & Challenger (division-less).
    """

    ONE = "I"
    TWO = "II"
    THREE = "III"
    FOUR = "IV"