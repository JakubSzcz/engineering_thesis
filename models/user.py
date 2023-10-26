from pydantic import BaseModel


# REQUEST
class GetUserReq(BaseModel):
    username: str
    password: str