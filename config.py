from redis.commands.search.field import TextField, NumericField, TagField

# LINKS
EXP_IP = "exp_api"
PROC_IP = "proc_api"
SYS_IP = "sys_api"
POSTGRES_IP = "postgresdb_clean"
MONGO_IP = "mongodb_clean"
REDIS_IP = "redisdb_clean"

# PORTS
EXP_PORT = "8080"
PROC_PORT = "8081"
SYS_PORT = "8082"

# SERVER LISTEN
EXP_SERV = "0.0.0.0"
PROC_SERV = "0.0.0.0"
SYS_SERV = "0.0.0.0"

# SECRET
EXP_SEC = ""
PROC_SEC = ""
SYS_SEC = ""

# POSTGRES
PG_PSW = "postgres"
PG_PORT = 5432
PG_USR = "postgres"
PG_HOST = POSTGRES_IP
PG_DB = "postgres_db"

# MONGODB
MDB_PORT = 27017
MDB_HOST = MONGO_IP
MDB_DB = "mongo_db"
MDB_PSW = "mongo"

# REDIS
REDIS_PORT = 6379
REDIS_HOST = REDIS_IP
REDIS_DB = "redis"  # not used
REDIS_PSW = "redis"  # not used

# OPENAPI
sys_description = """
System API purpose is to process all database engines operations and error handling.
## System API is responsible for:
* **Return user info directly from database**
* **Create user instance directly in database**
* **Directly deletes user from database** 
* **Verify if user exist in database** 
* **Process testing database requests**
"""
tags_metadata_sys_api = [
    {
        "name": "PostgreSQL",
        "description": "Manage all PostgreSQL related operations.",
    },
    {
        "name": "MongoDB",
        "description": "Manage all MongoDB related operations.",
    },
    {
        "name": "Redis",
        "description": "Manage all Redis related operations.",
    },
    {
        "name": "SQLite3",
        "description": "Manage all SQLite3 related operations.",
    }
]

# DATABASES
tables_names = ["title_basics", "name_basics", "title_episodes"]
# POSTGRES
tables_create_psql = {
    "title_basics": "CREATE TABLE title_basics (tconst VARCHAR(255) PRIMARY KEY, titleType VARCHAR(255), primaryTitle "
                    "VARCHAR(300), originalTitle VARCHAR(300), isAdult BOOLEAN, startYear INTEGER, endYear INTEGER, "
                    "runtimeMinutes INTEGER, genres VARCHAR(255));",
    "name_basics": "CREATE TABLE name_basics (nconst VARCHAR(255) PRIMARY KEY, primaryName VARCHAR(255), birthYear "
                  "INTEGER, deathYear INTEGER, primaryProfession VARCHAR(255)[3], "
                  "knownForTitles VARCHAR(255)[]);",
    "title_episodes": "CREATE TABLE title_episodes (tconst VARCHAR(255) PRIMARY KEY, parentTconst VARCHAR(255) "
                      ", seasonNumber INTEGER, episodeNumber INTEGER);"
}
tables_insert_psql = {
    "title_basics": "INSERT INTO title_basics (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, "
                    "endYear, runtimeMinutes, genres) VALUES (\'{tconst}\', \'{titleType}\', \'{primaryTitle}\',"
                    " \'{originalTitle}\', \'{isAdult}\', \'{startYear}\', \'{endYear}\',"
                    " \'{runtimeMinutes}\', \'{genres}\')",
    "name_basics": "INSERT INTO name_basics (nconst, primaryName, birthYear, deathYear, primaryProfession, "
                   "knownForTitles) VALUES (\'{nconst}\', \'{primaryName}\', \'{birthYear}\',"
                  " \'{deathYear}\', ARRAY {primaryProfession}, ARRAY {knownForTitles})",
    "title_episode": "INSERT INTO title_episodes (tconst, parentTconst, seasonNumber, episodeNumber)"
                  " VALUES (\'{tconst}\', \'{parentTconst}\', \'{seasonNumber}\',"
                    " \'{episodeNumber}\')"
}

# REDIS
indexes_create_schema = {
    "title_basics": {
        "schema": [
            TextField(name='tconst'),
            TextField(name='titleType'),
            TextField(name='primaryTitle'),
            TextField(name='originalTitle'),
            NumericField(name='isAdult'),
            NumericField(name='startYear'),
            NumericField(name='endYear'),
            NumericField(name='runtimeMinutes'),
            TextField(name='genres')
        ],
        "prefix": "title_basics:"
    },
    "name_basics": {
        "schema": [
            TextField(name='nconst'),
            TextField(name='primaryName'),
            NumericField(name='birthYear'),
            NumericField(name='deathYear'),
            TagField(name='primaryProfession'),
            TagField(name='knownForTitles')
        ],
        "prefix": "name_basics:"
    },
    "title_episodes": {
        "schema": [
            TextField(name='tconst'),
            TextField(name='parentTconst'),
            NumericField(name='seasonNumber'),
            NumericField(name='episodeNumber')
        ],
        "prefix": "title_episodes:"
    },
    "users": {
        "schema": (
            TextField(name='username'),
            TextField(name='password_hashed'),
            TextField(name='is_admin'),
            TextField(name='creation_date')
        ),
        "prefix": "user:"
    }
}

# SQLITE
tables_create_sqli = {
    "title_basics": "CREATE TABLE title_basics ( tconst TEXT PRIMARY KEY, titleType TEXT, primaryTitle "
                    "TEXT, originalTitle TEXT, isAdult INTEGER, startYear INTEGER, endYear INTEGER, "
                    "runtimeMinutes INTEGER, genres TEXT);",
    "name_basics": "CREATE TABLE name_basics (nconst TEXT PRIMARY KEY, primaryName TEXT, birthYear "
                  "INTEGER, deathYear INTEGER, primaryProfession TEXT[], "
                  "knownForTitles TEXT[]);",
    "title_episodes": "CREATE TABLE title_episodes (tconst TEXT PRIMARY KEY, parentTconst TEXT "
                      ", seasonNumber INTEGER, episodeNumber INTEGER);",
    "users": "CREATE TABLE users (user_id INTEGER PRIMARY KEY ASC, username TEXT UNIQUE, password_hashed TEXT, "
               "is_admin INTEGER, creation_date TEXT)"
}
tables_insert_sqli = {
    "title_basics": "INSERT INTO title_basics (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, "
                    "endYear, runtimeMinutes, genres) VALUES (\'{tconst}\', \'{titleType}\', \'{primaryTitle}\',"
                    " \'{originalTitle}\', \'{isAdult}\', \'{startYear}\', \'{endYear}\',"
                    " \'{runtimeMinutes}\', \'{genres}\')",
    "name_basics": "INSERT INTO name_basics (nconst, primaryName, birthYear, deathYear, primaryProfession, "
                   "knownForTitles)"
                  " VALUES (\'{nconst}\', \'{primaryName}\', \'{birthYear}\',"
                  " \'{deathYear}\', \'{primaryProfession}\', \'{knownForTitles}\')",
    "title_episodes": "INSERT INTO title_episodes (tconst, parentTconst, seasonNumber, episodeNumber)"
                  " VALUES (\'{tconst}\', \'{parentTconst}\', \'{seasonNumber}\', \'{episodeNumber}\')"
}


# DATA IMPORTS
title_basics_path = "../../bazy/title.basics.tsv/data_url_psql.tsv"
name_basics_path = "../../bazy/name.basics.tsv/data_url_psql.tsv"
title_episodes_path = "../../bazy/title.episode.tsv/data_url_psql.tsv"
