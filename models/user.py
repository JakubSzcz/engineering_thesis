from enum import Enum


# DATABASE
class DatabaseType(Enum):
    REDIS = "Redis",
    PSQL = "psql",
    MDB = "MongoDB"
    SQLi = "SQLite"
