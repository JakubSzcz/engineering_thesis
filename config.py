# LINKS
EXP_IP = "exp_api"
PROC_IP = "proc_api"
SYS_IP = "sys_api"
POSTGRES_IP = "postgresdb"
MONGO_IP = "mongodb"
REDIS_IP = "redisdb"

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


# JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 3600  # 15 minutes
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = "39B14A7C47F4AE6B1DC365B8F341E1A0F33D7B41662E3274E427DD3B227E49A1"
JWT_ISS = "http://" + PROC_IP + "/proc_api"

# OPENAPI
proc_description = """
Process API purpose is to process all request from exp_api, route them to correct endpoints of sys_api, generates all 
required information and handle errors.
## Process API is responsible for:
* **Generate JWT tokens** 
* **Validate user credentials** 
* **Routes exp_api requests**
* **Database data request handling** (_not implemented_).
"""
tags_metadata_proc_api = [
    {
        "name": "Authorization",
        "description": "Manage authorization related operations, like token generation.",
    },
    {
        "name": "Users",
        "description": "User related operations to all databases like insert, delete and read",
    },
    {
        "name": "Process",
        "description": "Data processor endpoints",
    }
]

# DATABASES
tables_names = ["title_basics", "name_basics", "title_episodes"]
db_types = ["redis", "mdb", "psql", "sqlite"]

models_fields = {
    "title_basics": "titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres",
    "name_basics": "primaryName, birthYear, deathYear, primaryProfession, knownForTitles",
    "title_episodes": "parentTconst, seasonNumber, episodeNumber"
}
