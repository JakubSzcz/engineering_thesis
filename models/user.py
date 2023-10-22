from datetime import datetime
from pydantic import BaseModel
from enum import Enum

# RESPONSES


# REQUESTS


# DATABASE
class DatabaseType(Enum):
    REDIS = "Redis",
    PSQL = "PostgreSQL",
    MDB = "MongoDB"
    SQLi = "SQLite"


class User(BaseModel):
    client_id: str
    client_secret: str
    admin: bool = False
    token: str
    creation_date: datetime = datetime.now()
    id: int
    database_type: DatabaseType


class CachedUserInfo(BaseModel):
    expiration_date: datetime
    client_id: str


class UserResponse(BaseModel):
    client_id: str
    client_secret: str
    timestamp: datetime


