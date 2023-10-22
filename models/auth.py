# imports
from pydantic import BaseModel, Field
from datetime import datetime


# RESPONSE
class Token(BaseModel):
    access_token: str = Field(description="Unique token generate for single user in order to allow communication with a"
                                          "server. Last symbol of the token determines engine used to store user data. "
                                          "Token is only valid for a specified period of time",
                              min_length=16, max_length=24, title="Token", examples=["abcdefgh12345678"])
    token_type: str = Field(description="Type of token used in authorization process, which is Bearer token",
                            title="Token type", examples=["Bearer token"])
    expiatory_time: datetime = Field(description="Expiration date of the token", title="Expiatory time",
                                     examples=["2023-10-22T12:43:16.857Z"])


class IsAuthenticatedRes(BaseModel):
    is_authenticated: bool
    client_id: str
    details: str | None = None
    token: Token | None = None
    already_auth_flag: bool | None = None


# REQUEST
class UserAuthReq(BaseModel):
    client_secret_hashed: str
    client_id: str
    timestamp: datetime

# DATABASE


class CachedTokenInfo(BaseModel):
    expiration_date: datetime
    token: str


