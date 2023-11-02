# libraries imports
from datetime import datetime

import redis
from redis.commands.search.field import TextField
from fastapi import APIRouter, Header, HTTPException, Query, Body
from typing import Annotated, List
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query as redisQuery

# packages imports
from models import user
from config import *


# ### variables ###
redis_router = APIRouter(
    prefix="/redis",
    tags=["Redis"]
)
# create redis instance
try:
    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
except redis.exceptions.ConnectionError as e:
    print("[ERROR] Can not connect to the database")
    raise HTTPException(
        status_code=500,
        detail="Can not connect to the database"
    )
# create indexes
# user index
try:
    users = r.ft("idx:users")
    # user exist
    users.info()
    print("[INFO] User index already exists. Data loaded.")
except redis.exceptions.ResponseError:
    schema = (
        TextField(name='username'),
        TextField(name='password_hashed'),
        TextField(name='is_admin'),
        TextField(name='creation_date')
    )
    users = r.ft("idx:users").create_index(schema, definition=IndexDefinition(index_type=IndexType.HASH,
                                                                              prefix=["user:"]))
    print("[INFO] New index for users created")


# ### functions ###


# ### endpoints ###
@redis_router.get("/user/validate", description="Validates whether user exists in Redis",
                 response_description="Returns flag and hashed_password if user exists", status_code=200)
async def validate_user(
        user_username: Annotated[str, Header(example="abcdefgh12345678", min_length=16, max_length=32,
                                             title="Client username", description="Unique char sequence provided by the"
                                                                                  " client in order to"
                                                                                  " identifies users")]
) -> user.UserExistsRes:
    # retrieve data from db
    try:
        db_response = users.search(redisQuery(f"@username:{user_username}"))
    except redis.exceptions.ConnectionError:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    # send response
    if len(db_response.docs) == 0:
        return user.UserExistsRes(exist=False)
    else:
        return user.UserExistsRes(exist=True, password_hashed=db_response.docs[0]["password_hashed"])


@redis_router.get("/user", description="Returns all the information stored about users or specified user",
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
            db_response = users.search(redisQuery("*"))
        except redis.exceptions.ConnectionError:
            print("[ERROR] Can not connect to the database")
            raise HTTPException(
                status_code=500,
                detail="Can not connect to the database"
            )
        if len(db_response.docs) == 0:
            raise HTTPException(
                status_code=404,
                detail="User database is empty",
            )

        # prepare list of users to return
        users_to_return = []
        for user_db in db_response.docs:
            user_db = user_db.__dict__
            users_to_return.append(user.GetUserInfoRes(
                user_id=str(user_db["id"]).split(":")[1], username=user_db["username"],
                is_admin=user_db["is_admin"], creation_date=user_db["creation_date"]))
        return users_to_return
    # if username was provided
    else:
        # execute query, fetch response and close connection
        db_response = users.search(redisQuery(f"@username:{username}"))
        if len(db_response.docs) == 0:
            raise HTTPException(
                status_code=404,
                detail="No user with a such username"
            )
        db_response = db_response.docs[0]
        # return response
        return user.GetUserInfoRes(
                user_id=str(db_response["id"]).split(":")[1], username=db_response["username"],
                is_admin=db_response["is_admin"], creation_date=db_response["creation_date"])


@redis_router.post("/user", status_code=201, description="Create new user")
async def insert_user(
        username: Annotated[str, Body(title="Username", description="Unique user username",
                                      examples=["text_test_test_test1"])],
        password_hash: Annotated[str, Body(title="Password", description="Unique user username",
                                           examples=["sadasdasdasdasd"])]
):
    try:
        r.hset(name=("user:" + str(int(datetime.now().timestamp()))), mapping={
            "username": username, "password_hashed": password_hash,
            "is_admin": str(False), "creation_date": str(datetime.utcnow())})
    except redis.exceptions.ConnectionError:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    return {"message": "New user created in Redis"}


@redis_router.delete("/user", status_code=200, description="Delete user from the database by the username")
async def insert_user(
        username: Annotated[str, Query(title="Username", description="Unique user username",
                                       examples=["text_test_test_test1"])],
):
    # connect to the database and execute query
    try:
        db_response = users.search(redisQuery(f"@username:{username}"))
        if len(db_response.docs) != 0:
            r.hdel(str(db_response.docs[0]["id"]), "username", "password_hashed", "is_admin", "creation_date")
        else:
            raise HTTPException(
                status_code=404,
                detail="No user with a such username"
            )
    except redis.exceptions.ConnectionError:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    return {"message": "User deleted from Redis"}
