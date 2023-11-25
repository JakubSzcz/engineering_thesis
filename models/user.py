# contains models of responses/requests connected with user related operations

# library imports
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


# RESPONSE
class GetUserInfoRes(BaseModel):
    user_id: int | str = Field(title="User id", description="Unique identificator of user", example=1)
    username: str = Field(title="User username", description="Unique username of user",
                          example="jkdnasjknjkkj22nkjk1")
    is_admin: bool = Field(title="Is user an admin", description="Indicator of admin rights", examples=[True])
    creation_date: datetime = Field(title="Creation date", description="Date of accounts creation",
                                    example="2023-10-24T17:13:07.909934")


class UserToExpRes(BaseModel):
    users: GetUserInfoRes | List[GetUserInfoRes] = Field(title="User info", description="Response from database",
                                                         example=
    [GetUserInfoRes(user_id=1, username="test1", is_admin=False, creation_date="2023-10-24T17:13:07.909934"),
     GetUserInfoRes(user_id=2, username="test2", is_admin=False, creation_date="2023-11-24T17:13:07.909934")])


class CreateUserRes(BaseModel):
    username: str = Field(title="User username", description="Unique username of user",
                          example="jkdnasjknjkkj22nkjk1")
    password: str = Field(title="User password", description="User password",
                          example="jkdnasjknjkkj22nkjk1")
