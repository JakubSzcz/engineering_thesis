# libraries imports
from fastapi import APIRouter, Header, HTTPException, Query, Body, responses
from typing import Annotated, List
import pymongo
from pymongo import MongoClient
from datetime import datetime

from pymongo.errors import ServerSelectionTimeoutError

# packages imports
from models import user
from config import *


# ### variables ###
mdb_router = APIRouter(
    prefix="/mdb",
    tags=["MongoDB"],
)

try:
    # mongo client
    client = MongoClient(MDB_HOST, MDB_PORT)
    # mongo database
    db = client[MDB_DB]
    # define collection
    users = db["users"]
except ServerSelectionTimeoutError as e:
    print("[ERROR] Can not connect to the database")
    raise e


# ### endpoints ###
@mdb_router.get("/user/validate", description="Validates whether user exists in MongoDB",
                 response_description="Returns flag and hashed_password if user exists", status_code=200)
async def validate_user(
        user_username: Annotated[str, Header(example="abcdefgh12345678", min_length=16, max_length=32,
                                             title="Client username", description="Unique char sequence provided by the"
                                                                                  " client in order to"
                                                                                  " identifies users")]
) -> user.UserExistsRes:
    # retrieve data from db
    try:
        db_response = users.find_one({"username": user_username})
    except ServerSelectionTimeoutError:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    # send response
    if db_response is None:
        return user.UserExistsRes(exist=False)
    else:
        return user.UserExistsRes(exist=True, password_hashed=db_response["password_hashed"])


@mdb_router.get("/user", description="Returns all the information stored about users or specified user",
                response_description="Returns information retrieved from the database", status_code=200)
async def get_user_info(
        username: Annotated[str | None, Query(title="Username",
                                              description="Username by which you can retrieve its info from database")]
        = None) -> user.GetUserInfoRes | List[user.GetUserInfoRes]:
    # if username was not provided select all users
    if username is None:
        # handle errors
        try:
            # execute query, fetch response and close connection
            db_response = users.find()
        except ServerSelectionTimeoutError:
            print("[ERROR] Can not connect to the database")
            raise HTTPException(
                status_code=500,
                detail="Can not connect to the database"
            )

        if len(list(db_response.clone())) == 0:
            raise HTTPException(
                status_code=404,
                detail="User database is empty",
            )

        # prepare list of users to return
        users_to_return = []
        for user_db in list(db_response):
            users_to_return.append(user.GetUserInfoRes(
                user_id=str(user_db["_id"]), username=user_db["username"],
                is_admin=user_db["is_admin"], creation_date=user_db["creation_date"]))
        return users_to_return
    # if username was provided
    else:
        # execute query, fetch response and close connection
        db_response = users.find_one({"username": username})
        if db_response is None:
            raise HTTPException(
                status_code=404,
                detail="No user with a such username"
            )
        # return response
        return user.GetUserInfoRes(
                user_id=str(db_response["_id"]), username=db_response["username"],
                is_admin=db_response["is_admin"], creation_date=db_response["creation_date"])


@mdb_router.post("/user", status_code=201, description="Create new user")
async def insert_user(
        username: Annotated[str, Body(title="Username", description="Unique user username",
                                      examples=["text_test_test_test1"])],
        password_hash: Annotated[str, Body(title="Password", description="Unique user username",
                                           examples=["sadasdasdasdasd"])]
):
    try:
        users.insert_one({"username": username, "password_hashed": password_hash,
                      "is_admin": False, "creation_date": datetime.utcnow()})
    except ServerSelectionTimeoutError:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    return {"message": "New user created in MongoDB"}


@mdb_router.delete("/user", status_code=200, description="Delete user from the database by the username")
async def insert_user(
        username: Annotated[str, Query(title="Username", description="Unique user username",
                                       examples=["text_test_test_test1"])],
):
    # connect to the database and execute query
    try:
        if users.find_one({"username": username}):
            users.delete_one({"username": username})
        else:
            raise HTTPException(
                status_code=404,
                detail="No user with a such username"
            )
    except ServerSelectionTimeoutError:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    return {"message": "User deleted from MongoDB"}
