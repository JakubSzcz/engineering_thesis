from datetime import datetime
from pydantic import BaseModel
from enum import Enum

class Database_Type(Enum):
    REDIS = "Redis",
    PSQL = "PostgreSQL",
    MDB = "MongoDB"
class User(BaseModel):
    client_id: str
    client_secret: str
    admin: bool = False
    token: str
    timestamp: datetime
    id: int
    database_type: Database_Type
