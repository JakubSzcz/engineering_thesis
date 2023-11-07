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
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutes
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
