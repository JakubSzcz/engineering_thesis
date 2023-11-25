# contains all user related endpoints and operations
# prefix /users
# authorization required: False
# endpoints list:
#   -GET / - retrieve user/users info
#   -POST / - create new user
#   -DELETE / - delete user instance
# functions list:
#   -generate_random_string() - generates random string, used for client_id and password creation

# libraries imports
from fastapi import APIRouter, HTTPException, Query, Depends
from utilities import functions as fun
from typing import Annotated
import httpx
import secrets
import string
import random


# packages imports
from config import *
from models import user, openapi, http_custom_error


# ### variables ###
user_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)
hash_context = fun.HashContext()


# ### functions ###
def generate_random_string():
    # creates string that contains random alphanumeric characters
    character_set = string.ascii_letters + string.digits  # Alphanumeric characters
    random_string = ''.join(secrets.choice(character_set) for _ in range(25))

    return random_string


# ### endpoints ####
@user_router.get("", description="Request user info from sys_api", response_description="List of users",
                 status_code=200,
                 responses={
                     404: openapi.no_username_found,
                     500: openapi.cannot_connect_to_sys_api
                 })
async def get_user(
    db_type: Annotated[str, Depends(fun.validate_db_type)],
    username: Annotated[str | None, Query(title="Username", description="Username by which you can retrieve "
                                                                        "its info from database")] = None
) -> user.UserToExpRes:

    # send request to the sys api
    async with httpx.AsyncClient() as client:
        try:
            # all users
            if username is None:
                response = await client.get(
                    url=fun.compose_url(SYS_IP, SYS_PORT) + "/" + db_type + "/users"
                )
            # single user by username
            else:
                response = await client.get(
                    url=fun.compose_url(SYS_IP, SYS_PORT) + "/" + db_type + "/users",
                    params=httpx.QueryParams({
                        "username": username,
                    })
                )
        # no connection to the sys api handling
        except httpx.ConnectError:
            raise http_custom_error.cannot_connect_to_sys

        # handling errors
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["detail"]
            )
        else:
            if username is None:
                return user.UserToExpRes(users=[user.GetUserInfoRes(**item) for item in response.json()])
            else:
                return user.UserToExpRes(users=user.GetUserInfoRes(**response.json()))


@user_router.post("", status_code=201, description="Creates a new user in the database",
                  response_description="Returns credentials: username and password",
                  responses={
                      500: openapi.cannot_connect_to_sys_api
                  })
async def create_user(
    db_type: Annotated[str, Depends(fun.validate_db_type)]
) -> user.CreateUserRes:

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
                url=fun.compose_url(SYS_IP, SYS_PORT) + "/" + db_type + "/users",
                json=data
            )
        # no connection to the sys api handling
        except httpx.ConnectError:
            raise http_custom_error.cannot_connect_to_sys

    # return response
    if response.status_code == 201:
        return user.CreateUserRes(username=username, password=password)
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"]
        )


@user_router.delete("", status_code=200, description="Deletes user with provided username",
                    response_description="Deletion confirmation",
                    responses={
                        200: openapi.user_deleted,
                        404: openapi.no_username_found,
                        500: openapi.cannot_connect_to_sys_api
                    })
async def delete_user(
        db_type: Annotated[str, Depends(fun.validate_db_type)],
        username: Annotated[str, Query(title="Username", description="Username by which user will be deleted "
                                                                     "from the database")]
):

    async with httpx.AsyncClient() as client:
        try:
            # send request to the sys_api
            response = await client.delete(
                url=fun.compose_url(SYS_IP, SYS_PORT) + "/" + db_type + "/users",
                params=httpx.QueryParams({
                    "username": username,
                })
            )
        # no connection to the sys api handling
        except httpx.ConnectError:
            raise http_custom_error.cannot_connect_to_sys

    # hande response
    if response.status_code == 200:
        return {"message": "User deleted"}
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"]
        )
