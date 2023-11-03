# libraries import
from fastapi import APIRouter, Header, HTTPException, Path
from typing import Annotated
import httpx

# packages import
from config import *
from models import user
from models import openapi
from utilities import functions

# ### variables ###
user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)


# ### functions ###
def validate_db_type(db_type: str):
    if db_type not in ["REDIS", "MDB", "PSQL", "SQLi"]:
        raise HTTPException(
            status_code=400,
            detail="Wrong db_type, possible database types: REDIS, MDB, PSQL, SQLi"
        )


# ### endpoints ###
@user_router.get("/{username}", status_code=200, description="Retrieve user by it username",
                 response_description="User info from database",
                 responses={
                     400: openapi.wrong_db_type_header,
                     404: openapi.no_username_found,
                     500: openapi.cannot_connect_to_proc_api
                 })
async def retrieve_user(
        db_type: Annotated[str, Header(title="Database type", description="Select database you want to retrieve users "
                                                                          "info from: ['REDIS', 'MDB','PSQL', 'SQLi']",
                                       examples=["REDIS", "MDB","PSQL", "SQLi"])],
        username: Annotated[str, Path(title="User id", description="User username unique char sequence",
                                      example="test_test_test_test")]
) -> user.UserResponse:
    # validate database type provided
    validate_db_type(db_type)
    # send request to the proc_api
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url=functions.compose_url(PROC_IP, PROC_PORT) + "/user?username=" + username,
                headers=httpx.Headers({
                    "db-type": db_type,
                })
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=500,
                detail="Cannot connect to the proc_api"
            )
    # handle response and errors
    if response.status_code == 200:
        return user.UserResponse(**response.json()["users"])
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"]
        )


@user_router.get("", status_code=200, description="Retrieve all users info from the specified database",
                 response_description="List of users stored in the database",
                 responses={
                     400: openapi.wrong_db_type_header,
                     500: openapi.cannot_connect_to_proc_api
                 })
async def retrieve_all_users(
        db_type: Annotated[str, Header(title="Database type", description="Select database you want to retrieve users "
                                                                          "info from", examples=["REDIS", "MDB",
                                                                                                 "PSQL", "SQLi"])]
) -> user.GetUsersInfoRes:
    # validate database type provided
    validate_db_type(db_type)
    # send request to the proc_api
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url=functions.compose_url(PROC_IP, PROC_PORT) + "/user",
                headers=httpx.Headers({
                    "db-type": db_type,
                })
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=500,
                detail="Cannot connect to the proc_api"
            )
    # handle response, create users list, handle errors
    if response.status_code == 200:
        return user.GetUsersInfoRes(users=[user.UserResponse(**item) for item in response.json()["users"]])
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"]
        )


@user_router.delete("/{username}", status_code=200, description="Deletes user with provided username",
                    responses={
                        200: openapi.user_deleted,
                        400: openapi.wrong_db_type_header,
                        404: openapi.no_username_found,
                        500: openapi.cannot_connect_to_proc_api
                    })
async def delete_user(
        db_type: Annotated[str, Header(title="Database type", description="Select database you want to store user info"
                                                                          "info from", examples=["REDIS", "MDB",
                                                                                                 "PSQL", "SQLi"])],
        username: Annotated[str, Path(title="User id", description="User username unique char sequence",
                                      example="test_test_test_test")]
):
    validate_db_type(db_type)

    # send request to the proc_api
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(
                url=functions.compose_url(PROC_IP, PROC_PORT) + "/user?username=" + username,
                headers=httpx.Headers({
                    "db-type": db_type,
                })
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=500,
                detail="Cannot connect to the proc_api"
            )
    # handle response
    if response.status_code == 200:
        return {"message": "User deleted"}
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"]
        )


@user_router.post("", status_code=201, description="Creates user into provided database",
                  response_description="Returns username and password",
                  responses={
                      400: openapi.wrong_db_type_header,
                      500: openapi.cannot_connect_to_proc_api
                  })
async def create_user(
        db_type: Annotated[str, Header(title="Database type", description="Select database you want to store user info"
                                                                          "info from", examples=["REDIS", "MDB",
                                                                                                 "PSQL", "SQLi"])]
) -> user.CreateUserRes:
    # validate database type provided
    validate_db_type(db_type)
    # send request to the proc_api
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url=functions.compose_url(PROC_IP, PROC_PORT) + "/user",
                headers=httpx.Headers({
                    "db-type": db_type,
                })
            )
        except httpx.ConnectError:
            raise HTTPException(
                status_code=500,
                detail="Cannot connect to the proc_api"
            )
    # handle response and errors
    if response.status_code == 201:
        return user.CreateUserRes(**response.json())
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"]
        )
