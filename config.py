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
ACCESS_TOKEN_EXPIRE_MINUTES = 360  # 30 minutes
JWT_ALGORITHM = "HS256"
JWT_SECRET_KEY = "39B14A7C47F4AE6B1DC365B8F341E1A0F33D7B41662E3274E427DD3B227E49A1"
JWT_ISS = "http://" + PROC_IP + "/proc_api"

# DATABASE PREPARATION
title_basics_path = "../../bazy/title.basics.tsv/data.tsv"
title_basics_path_url = "../../bazy/title.basics.tsv/data_url_{db_type}.{file_ext}"
name_basics_path = "../../bazy/name.basics.tsv/data.tsv"
name_basics_path_url = "../../bazy/name.basics.tsv/data_url_{db_type}.{file_ext}"
title_episodes_path = "../../bazy/title.episode.tsv/data.tsv"
title_episodes_path_url = "../../bazy/title.episode.tsv/data_url_{db_type}.{file_ext}"
test_path = "../../bazy/title.basics.tsv/redis_test.tsv"
test_path_url = "../../bazy/title.basics.tsv/test_url_{db_type}.{file_ext}"
