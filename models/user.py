from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum
from typing import List


# RESPONSES
class UserResponse(BaseModel):
    user_id: int | str = Field(title="User id", description="Unique identificator of user", example=1)
    username: str = Field(title="User username", description="Unique username of user",
                          example="jkdnasjknjkkj22nkjk1")
    is_admin: bool = Field(title="Is user an admin", description="Indicator of admin rights", examples=[True])
    creation_date: datetime = Field(title="Creation date", description="Date of accounts creation",
                                    example="2023-10-24T17:13:07.909934")


class GetUsersInfoRes(BaseModel):
    users: UserResponse | List[UserResponse] = Field(title="User info", description="Response from database",
                                                     examples=[[
    [UserResponse(user_id=1, username="test", is_admin=False, creation_date="2023-10-24T17:13:07.909934"),
     UserResponse(user_id=2, username="test2", is_admin=False, creation_date="2023-11-24T17:13:07.909934")]],
     UserResponse(user_id=1, username="test", is_admin=False, creation_date="2023-10-24T17:13:07.909934")])


class CreateUserRes(BaseModel):
    message: str = "New user created"
    username: str = Field(title="User username", description="Unique username of user",
                          example="jkdnasjknjkkj22nkjk1")
    password: str = Field(title="User password", description="User password",
                          example="jkdnasjknjkkj22nkjk1")

# REQUESTS


# DATABASE
class DatabaseType(str, Enum):
    REDIS = "redis",
    PSQL = "psql",
    MDB = "mdb"
    SQLi = "sqlite"


class CachedUserInfo(BaseModel):
    expiration_date: datetime
    client_id: str
