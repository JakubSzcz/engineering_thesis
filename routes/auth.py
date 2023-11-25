# contains authorization related endpoints and functions
# prefix: /auth
# authorization required: False
# endpoints list:
#   -GET /token - generates token for the provided user credentials
# function list:
#   -is_user_authenticated(token) - validates whether user with the provided token has been authorized

# library imports
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime
from jose import jwt, exceptions
from pydantic import ValidationError
import httpx

# packages imports
from models import auth, openapi, http_custom_error
from cache import Cache
from utilities import functions as fun
from config import *

# ### variables ####
hash_context = fun.HashContext()
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
cache = Cache()


# ### functions ####
async def is_user_authenticated(token: Annotated[str, Depends(oauth2_scheme)]) -> bool:
    # decodes provided token and validates whether it is valid and not expired
    # params:
    # @token - Dependency injection of the Bearer access token from oauth2_schema
    # returns True if user is authenticated or False otherwise

    # decode token
    try:
        jwt_payload = jwt.decode(
            token=token, key=JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM]
        )
    # raise validation error if token is invalid
    except (exceptions.JWTError, ValidationError):
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
@auth_router.post("/token", description="Endpoints for creation process of the token", status_code=201,
                  response_description="Returns access token with its expiration time",
                  responses={
                    400: openapi.wrong_db_type_header,
                    401: openapi.incorrect_credentials,
                    404: openapi.no_username_found,
                    500: openapi.cannot_connect_to_proc_api
                  })
async def get_token(form: Annotated[OAuth2PasswordRequestForm, Depends()]) -> auth.Token:
    # gets injected the OAuth2 password form as dependency

    timestamp = datetime.utcnow()
    # check if user exist in database
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url=fun.compose_url(PROC_IP, PROC_PORT) + "/auth/user",
                headers=httpx.Headers({
                    "user-username": form.username,
                    "user-password-plain": form.password,
                    "timestamp": timestamp.strftime('%Y-%m-%d %H:%M:%S')
                })
            )
        except httpx.ConnectError:
            raise http_custom_error.cannot_connect_to_proc

    # handling errors
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
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
