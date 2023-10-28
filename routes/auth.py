# ### imports ####
import jose.exceptions
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime
import httpx
from jose import jwt
from pydantic import ValidationError

from models import auth
from cache import Cache
from utilities import functions
from config import *

# ### variables ####
hash_context = functions.HashContext()
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
cache = Cache()


# ### functions ####
async def is_user_authenticated(token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    try:
        jwt_payload = jwt.decode(
            token=token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
    # raise validation error if token is invalid
    except (jose.exceptions.JWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # raise error if token is expired
    if datetime.fromtimestamp(jwt_payload["exp"]) < datetime.utcnow():
        raise HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return True


# ### endpoints###
@auth_router.post("/token", description="Endpoints for creation of token", status_code=201,
                  response_description="Returns access token with its expiration time")
async def get_token(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> auth.Token:
    timestamp = datetime.utcnow()
    # check if user exist in database
    async with httpx.AsyncClient() as client:
        try:
            # TODO signing request
            response = await client.get(
                url=functions.compose_url(PROC_IP, PROC_PORT) + "/auth/user",
                headers=httpx.Headers({
                    "user-username": form.username,
                    "user-password-plain": form.password,
                    "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=500,
                detail="Cannot connect to the proc_api"
            )

    # handling errors
    if response.status_code != 200:
        raise HTTPException(
            status_code=400,
            detail=response.json()["detail"]
        )

    response = response.json()

    # handling response
    if not response["exist"]:
        raise HTTPException(
            status_code=401,
            detail="Incorrect credentials or client does not exists"
        )
    else:
        if not response["correct_pwd"]:
            raise HTTPException(
                status_code=401,
                detail="Incorrect password"
            )
        else:
            return auth.Token(**response["token"])


@auth_router.get("/test", dependencies=[Depends(is_user_authenticated)])
def test_connection():
    return "to access this endpoint you have to be authorized, and you are"
