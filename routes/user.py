# libraries imports
import random
from fastapi import APIRouter, Header, HTTPException, Query
from utilities import functions
from typing import Annotated
import httpx
import secrets
import string


# packages imports
from config import *
from models.user import *


# ### variables ###
user_router = APIRouter(
    prefix="/user",
    tags=["Users"],
)
hash_context = functions.HashContext()


# ### functions ###
def generate_random_string():
    character_set = string.ascii_letters + string.digits  # Alphanumeric characters
    random_string = ''.join(secrets.choice(character_set) for _ in range(25))

    return random_string


# ### endpoints ####
@user_router.get("", description="Request user info from sys_api", response_description="List of users",
                 status_code=200)
async def get_user(
    db_type: Annotated[str, Header(title="Database type",
                                   description="Select database you want to retrieve users info from",
                                   examples=["REDIS", "MDB", "PSQL", "SQLi"])],
    username: Annotated[str | None, Query(title="Username", description="Username by which you can retrieve "
                                                                        "its info from database")] = None
) -> UserToExpRes:
    # send request to the sys api
    async with httpx.AsyncClient() as client:
        try:
            # all users
            if username is None:
                response = await client.get(
                    url=functions.compose_url(SYS_IP, SYS_PORT) + "/" + DatabaseType[db_type].value + "/user"
                )
            # single user by username
            else:
                response = await client.get(
                    url=functions.compose_url(SYS_IP, SYS_PORT) + "/" + DatabaseType[db_type].value + "/user",
                    params=httpx.QueryParams({
                        "username": username,
                    })
                )
        # no connection to the sys api handling
        except httpx.ConnectError:
            raise HTTPException(
                status_code=500,
                detail="Cannot connect to the sys_api"
            )

        # handling errors
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["detail"]
            )
        else:
            if username is None:
                return UserToExpRes(users=[GetUserInfoRes(**item) for item in response.json()])
            else:
                return UserToExpRes(users=GetUserInfoRes(**response.json()))


@user_router.post("", status_code=201, description="Creates a new user in the database",
                  response_description="Returns credentials: username and password")
async def create_user(
    db_type: Annotated[str, Header(title="Database type",
                                   description="Select database you want to retrieve users info from",
                                   examples=["REDIS", "MDB", "PSQL", "SQLi"])]
) -> CreateUserRes:

    # generate credentials accordingly to the database type
    username = generate_random_string()
    if db_type == "PSQL":
        username = username[:-1] + str(random.randint(0, 2))
    elif db_type == "MDB":
        username = username[:-1] + str(random.randint(3, 5))
    elif db_type == "REDIS":
        username = username[:-1] + str(random.randint(6, 7))
    else:
        username = username[:-1] + str(random.randint(8, 9))
    # generate password
    password = generate_random_string()
    # create data dic to be sent to the sys_api
    data = {
        "username": username,
        "password_hash": hash_context.create(password)
    }

    # send request to the sys api
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=functions.compose_url(SYS_IP, SYS_PORT) + "/" + DatabaseType[db_type].value + "/user",
                json=data
            )
        # no connection to the sys api handling
        except httpx.ConnectError:
            raise HTTPException(
                status_code=500,
                detail="Cannot connect to the sys_api"
            )
    # return response
    if response.status_code == 201:
        return CreateUserRes(username=username, password=password)
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"]
        )


@user_router.delete("", status_code=200, description="Deletes user with provided username",
                    response_description="None")
async def delete_user(
        db_type: Annotated[str, Header(title="Database type", description="Select database you want to retrieve users "
                                                                          "info from", examples=["REDIS", "MDB",
                                                                                                 "PSQL", "SQLi"])],
        username: Annotated[str, Query(title="Username", description="Username by which you can retrieve its "
                                                                     "info from database")]
):
    async with httpx.AsyncClient() as client:
        try:
            # send request to the sys_api
            response = await client.delete(
                url=functions.compose_url(SYS_IP, SYS_PORT) + "/" + DatabaseType[db_type].value + "/user",
                params=httpx.QueryParams({
                    "username": username,
                })
            )
        # no connection to the sys api handling
        except httpx.ConnectError:
            raise HTTPException(
                status_code=500,
                detail="Cannot connect to the sys_api"
            )
    # hande response
    if response.status_code == 200:
        return {"message": "User deleted"}
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"]
        )
