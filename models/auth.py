# Contains request/responses models connected with authorization process

# library imports
from pydantic import BaseModel, Field
from datetime import datetime


# RESPONSE
class Token(BaseModel):
    access_token: str = Field(description="Unique token generate for single user in order to allow communication with a"
                                          "server. Last symbol of the token determines engine used to store user data. "
                                          "Token is only valid for a specified period of time",
                              example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTgxNjI2MTEsInN1YiI6IjEyMyIsIml"
                                      "zcyI6Imh0dHA6Ly9sb2NhbGhvc3QvZXhwX2FwaSJ9.3cQhnsF3TOjyw"
                                      "PuFjwC8XLprfa3DXTmx5UD2f3bYZhw", title="Token")
    token_type: str = Field(description="Type of token used in authorization process, which is Bearer token",
                            title="Token type", examples=["Bearer token"])
    expiatory_time: datetime = Field(description="Expiration date of the token", title="Expiatory time",
                                     examples=["2023-10-22T12:43:16.857Z"])


class UserAuthRes(BaseModel):
    token: Token = Field(example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTgxNjI2MTEsInN1YiI6IjEyMyIsImlzcyI"
                                 "6Imh0dHA6Ly9sb2NhbGhvc3QvZXhwX2FwaSJ9.3cQhnsF3TOjywPuFjwC8XLprfa3DXTmx5UD2f3bYZhw",
                         description="Authentication token", default=None)
    exist: bool = Field(example=True, description="Informs if user was found in the database")
    correct_pwd: bool = Field(example=True, description="Informs if password was correct or not", default=None)
