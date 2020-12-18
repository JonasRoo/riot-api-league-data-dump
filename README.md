# Riot-API League of Legends Data Dump
A basic project setup to construct a real, representative dataset of an arbitrarily big dataset of **ranked** players.<br>
Given pre-defined desired distributions over servers, tiers and division, the [Riot API](https://developer.riotgames.com/apis#league-v4/GET_getLeagueEntries) `GET getLeagueEntries` is iterated until a full dataset is generated.<br>
The output medium (e.g. `csv`, `database`) can be selected.

# Features
- Exact number of players to fetch can be selected
- Distribution across ranks as well as servers can be customized
  > if not specified, a realistic pre-defined distributions is used
-  Rate limit of API keys are respected
- Output format can be chosen among:
  - csv
  - database (via `sqlalchemy` 👉 database can be any type)
- scraping across multiple servers is optimized (concurrent)

# Prerequisites
- A **working** Riot API key
- defined environment variables:
    > `X_RIOT_TOKEN`: your valid Riot Games API token.<br>
    > `RIOT_DATA_DUMP_DB_CONNECTION_STRING`: a valid SQLAlchemy databse connection string.

# Testing
Run `nosetests -v`