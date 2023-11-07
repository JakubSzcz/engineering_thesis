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
PG_PSW = "@mM&UmSZ}}3F99A8"
PG_PORT = "2020"
PG_USR = "postgres"

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 30 minutes
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = "39B14A7C47F4AE6B1DC365B8F341E1A0F33D7B41662E3274E427DD3B227E49A1"
JWT_ISS = "http://" + PROC_IP + "/proc_api"

# OPENAPI
exp_description = """
Experience API purpose is to handle all user related request and returns to users.
## Experience API is responsible for:
* **Create users** 
* **Read users** 
* **Delete users**
* **Generates token**
* **Insert data to Database** (_not implemented_).
* **Delete data from Database** (_not implemented_).
* **Queries data from Database** (_not implemented_).
"""
tags_metadata_exp_api = [
    {
        "name": "Administration panel",
        "description": "Admin operation such us direct access to the database resources"
    },
    {
        "name": "Authorization",
        "description": "Manage authorization related operations, like token generation."
    },
    {
        "name": "User",
        "description": "User related operations to all databases like insert, delete and read"
    },
    {
        "name": "Data",
        "description": "Databases related CRUD operation"
    }
]

# DATABASE
title_basics_path = "../../bazy/title.basics.tsv/data.tsv"
title_basics_path_url = "../../bazy/title.basics.tsv/data_url.tsv"
name_basics_path = "../../bazy/name.basics.tsv/data.tsv"
name_basics_path_url = "../../bazy/name.basics.tsv/data_url.tsv"
title_episodes_path = "../../bazy/title.episode.tsv/data.tsv"
title_episodes_path_url = "../../bazy/title.episode.tsv/data_url.tsv"
