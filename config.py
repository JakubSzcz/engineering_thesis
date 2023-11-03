# LINKS
EXP_IP = "localhost"
PROC_IP = "localhost"
SYS_IP = "localhost"

# PORTS
EXP_PORT = "8080"
PROC_PORT = "8081"
SYS_PORT = "8082"

# SERVER LISTEN
EXP_SERV = "localhost"
PROC_SERV = "localhost"
SYS_SERV = "localhost"

# SECRET
EXP_SEC = ""
PROC_SEC = ""
SYS_SEC = ""

# POSTGRES
PG_PSW = "postgres"
PG_PORT = "2020"
PG_USR = "postgres"
PG_HOST = "localhost"
PG_DB = "postgres_db"

# MONGODB
MDB_PORT = 2021
MDB_HOST = "localhost"
MDB_DB = "mongo_db"
MDB_PSW = "mongo"

# REDIS
REDIS_PORT = 2022
REDIS_HOST = "localhost"
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
* **Process testing database requests** (_not implemented_).
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
