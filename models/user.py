from pydantic import BaseModel, Field
from datetime import datetime


# REQUEST

# RESPONSE
class GetUserInfoRes(BaseModel):
    user_id: int | str = Field(title="User id", description="Unique identificator of user", example=1)
    username: str = Field(title="User username", description="Unique username of user",
                          example="jkdnasjknjkkj22nkjk1")
    is_admin: bool = Field(title="Is user an admin", description="Indicator of admin rights", examples=[True])
    creation_date: datetime = Field(title="Creation date", description="Date of accounts creation",
                                    example="2023-10-24T17:13:07.909934")


class UserExistsRes(BaseModel):
    exist: bool = Field(title="User exist flag", description="Informs if users exists in the database", examples=[True])
    password_hashed: str | None = Field(title="Hashed password", description="Hashed password string from the database",
                                 examples=["$.dsnaknkjgsnak>klsanlk@klnskal"], default=None)
