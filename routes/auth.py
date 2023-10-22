# ### imports ####
from fastapi import APIRouter, Depends, HTTPException, Body, Header
from typing import Annotated, List
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime
import pytz
import httpx

from models import auth
from models import user
from cache import Cache
from utilities import functions
from config import *

# ### variables ####
auth_router = APIRouter(
    prefix="/auth",
    tags=["Authorization"]
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# set timezone to UTC
datetime.now(pytz.timezone('UTC'))
cache = Cache()


# ### functions ####


def authenticate_user(client_id: str, client_secret_plain: str) \
        -> auth.IsAuthenticatedRes:
    timestamp = datetime.now()
    # check if user is already authenticated
    if cache.is_client_already_authenticated(client_id):
        return auth.IsAuthenticatedRes(is_authenticated=True, client_id=client_id,
                                       details="Client is already authorize. Please provide your token "
                                               "in order to access resource", already_auth_flag=True)

    # sending request to the proc api in order to auth user and generate token
    try:
        url = functions.compose_url(PROC_IP, PROC_PORT) + "/auth/user"
        with httpx.Client() as client:
            response = client.post(
                url,
                headers={
                    "Content-Type": "application/json",

                },
                data={
                    "client_id": client_id,
                    "client_secret_plain": client_secret_plain,
                    "timestamp": timestamp,

                }
            )
    except httpx.ConnectError:
        raise HTTPException(
            status_code=500,
            detail="Internal error. Cannot connect to the proc_api while authorization"
        )

    if response.status_code == 200:
        return auth.IsAuthenticatedRes(is_authenticated=True, client_id=client_id, token=response.json())
    else:
        return auth.IsAuthenticatedRes(is_authenticated=False, client_id=client_id, details="auth error details")


# ### routes ####
@auth_router.get("/token", response_model=auth.Token) # TO DO ADD ERRORS VALIDATION
def get_token(
        client_id: Annotated[str, Header(example="abcdefgh12345678", min_length=16, max_length=32,
                                         title="Client Secret",
                                         description="Unique char sequence provided by the client "
                                                     "in order to identifies users")],
        client_secret: Annotated[str, Header(example="abcdefgh12345678", min_length=16, max_length=32,
                                             title="Client password", description="Password provided by the client")]
):
    # authenticate user
    auth_context = authenticate_user(client_id, client_secret)
    if auth_context.is_authenticated and not auth_context.already_auth_flag:
        # add token and client_id to cash and return token
        cache.add_user_to_cache(user.CachedUserInfo(client_id=auth_context.client_id,
                                                    expiration_date=auth_context.token.expiatory_time))
        cache.add_token_to_cache(auth.CachedTokenInfo(token=auth_context.token.access_token,
                                                      expiration_date=auth_context.token.expiatory_time))
        return auth_context.token
    # handle already authenticated scenario
    elif auth_context.already_auth_flag:
        raise HTTPException(
            status_code=401,
            detail=auth_context.details,
            headers={"WWW-Authenticate": "Bearer"},
        )
    # not valid credentials scenario
    else:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )



