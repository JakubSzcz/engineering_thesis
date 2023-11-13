# libraries imports
from fastapi import APIRouter, Header, HTTPException
from utilities import functions as fun
from typing import Annotated, Any
from datetime import timedelta, datetime
import httpx
from jose import jwt


# packages imports
from config import *
from models import auth, openapi

# ### variables ###
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
)

# hash context
hash_context = fun.HashContext()


# ### functions ###
# function to generate jwt token
def creat_access_token(sub: str | Any, requested_time: datetime, exp_delta: int = None) -> (str, datetime):

    if exp_delta is None:
        expiry_time = requested_time + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    else:
        expiry_time = requested_time + timedelta(minutes=exp_delta)

    jwt_payload_to_encode = {
        "exp": expiry_time,  # expiry time of the token
        "sub": sub,  # unique id of client to whom token has been assigned
        "iss": JWT_ISS  # identifies the entity or system that created token

    }
    jwt_token = jwt.encode(jwt_payload_to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return jwt_token, expiry_time


# ### endpoints ###
@auth_router.get("/user", status_code=200, description="Verifies if user exist and if provided password is correct",
                 response_description="Returns flags if user exist and password if password is correct. "
                                      "If both of this are true, it returns access token",
                 responses={
                     404: openapi.no_username_found,
                     500: openapi.cannot_connect_to_sys_api
                 }
                 )
async def user_exists(
        user_username: Annotated[str, Header(example="abcdefgh12345678", min_length=16, max_length=32,
                                             title="Client username",
                                             description="Unique char sequence provided by the client in order "
                                                         "to identifies users")],
        user_password_plain: Annotated[str, Header(example="abcdefgh12345678", min_length=16, max_length=32,
                                                   title="Client password",
                                                   description="Plain password provided by the client")],
        timestamp: Annotated[datetime, Header(title="Timestamp", description="Timestamp of token request creation")]
) -> auth.UserAuthRes:

    # verify database destination by the last user_name char
    try:
        last_char = int(user_username[len(user_username)-1])
    except ValueError:
        raise HTTPException(
            status_code=500,
            detail="Last character in the username should be int in order to indentify db source"
        )
    # declare database type used
    if 0 <= last_char < 3:
        db_type = "psql"
    elif 3 <= last_char < 6:
        db_type = "mdb"
    elif 6 <= last_char < 8:
        db_type = "redis"
    else:
        db_type = "sqlite"

    # send request to the sys api to verify if user exists
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url=fun.compose_url(SYS_IP, SYS_PORT) + f"/{db_type}/user/validate",
                headers=httpx.Headers({
                    "user-username": user_username
                })
            )
        except httpx.ConnectError:
            print("[ERROR] Cannot connect to the sys_api")
            raise HTTPException(
                status_code=500,
                detail="Cannot connect to the sys_api"
            )
        # if users exists, verifies its password
        if bool(response.json()["exist"]):
            if hash_context.verify(user_password_plain, response.json()["password_hashed"]):
                token, expiry_time = creat_access_token(user_username, requested_time=timestamp)
                return auth.UserAuthRes(token=auth.Token(access_token=token, token_type="Bearer",
                                                         expiatory_time=expiry_time), exist=True, correct_pwd=True)
            else:
                return auth.UserAuthRes(exist=True, correct_pwd=False)
        else:
            return auth.UserAuthRes(exist=False)
