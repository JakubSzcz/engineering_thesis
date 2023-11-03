# libraries imports
from fastapi import APIRouter, Header, HTTPException, Query, Body
from typing import Annotated, List
from datetime import datetime
import os


# packages imports
from models import user, openapi
from SQL_engines.SQLite import SQLite

# ### variables ###
sqli_router = APIRouter(
    prefix="/sqlite",
    tags=["SQLite3"]
)
# connecting to the database file
db = SQLite()
if "sqlitedb.db" not in os.listdir("./SQL_engines"):
    db.connect()
    # create users database
    db.execute("CREATE TABLE users (user_id INTEGER PRIMARY KEY ASC, username TEXT UNIQUE, password_hashed TEXT, "
               "is_admin INTEGER, creation_date TEXT)")
    db.commit()
# ### functions ###


# ### endpoints ###
@sqli_router.get("/user/validate", description="Validates whether user exists in SQLite",
                 response_description="Returns flag and hashed_password if user exists", status_code=200)
async def validate_user(
        user_username: Annotated[str, Header(example="abcdefgh12345678", min_length=16, max_length=32,
                                             title="Client username", description="Unique char sequence provided by the"
                                                                                  " client in order to"
                                                                                  " identifies users")]
) -> user.UserExistsRes:
    # connect to the database
    db.connect()
    # execute query, fetch response and close connection
    db.execute(f"SELECT * FROM users WHERE username = '{user_username}'")
    db_response = db.get_query_results()
    db.commit()
    # check if user with such username exists
    # return response accordingly
    if not db_response:
        return user.UserExistsRes(exist=False)
    else:
        return user.UserExistsRes(exist=True, password_hashed=db_response[0][2])


@sqli_router.get("/user", description="Returns all the information stored about users or specified user",
                 response_description="Returns information retrieved from the database", status_code=200,
                 responses={
                     404: openapi.database_empty
                 })
async def get_user_info(
        username: Annotated[str | None, Query(title="Username",
                                              description="Username by which you can retrieve its info from database")]
        = None) -> user.GetUserInfoRes | List[user.GetUserInfoRes]:

    # connect to the database
    db.connect()
    # if username was not provided select all users
    if username is None:
        # execute query, fetch response and close connection
        db.execute(f"SELECT user_id, username, creation_date, is_admin FROM users")
        db_response = db.get_query_results()
        db.commit()
        if not db_response:
            raise HTTPException(
                status_code=404,
                detail="User database is empty"
            )
        # prepare list of users to return
        users = []
        for user_db in db_response:
            users.append(user.GetUserInfoRes(user_id=user_db[0], username=user_db[1],
                                             is_admin=user_db[3], creation_date=user_db[2]))
        return users
    # if username was provided
    else:
        # execute query, fetch response and close connection
        db.execute(f"SELECT user_id, username, creation_date, is_admin FROM users WHERE username = '{username}'")
        db_response = db.get_query_results()
        db.commit()
        if not db_response:
            raise HTTPException(
                status_code=404,
                detail="No user with a such username"
            )
        db_response = db_response[0]
        # return response
        return user.GetUserInfoRes(user_id=db_response[0], username=db_response[1],
                                   is_admin=db_response[3], creation_date=db_response[2])


@sqli_router.post("/user", status_code=201, description="Create new user",
                  responses={
                      201: openapi.new_user_created
                  })
async def insert_user(
        username: Annotated[str, Body(title="Username", description="Unique user username",
                                      examples=["text_test_test_test1"])],
        password_hash: Annotated[str, Body(title="Password", description="Unique user username",
                                           examples=["sadasdasdasdasd"])]
):
    timestamp = datetime.utcnow()
    # connect to the database and executes query
    db.connect()
    db.execute(f"INSERT INTO users (username, password_hashed, is_admin, creation_date) VALUES ('{username}', "
               f"'{password_hash}', 0, '{timestamp}');")
    db.commit()
    return {"message": "New user created in SQLite"}


@sqli_router.delete("/user", status_code=200, description="Delete user from the database by the username",
                    responses={
                        200: openapi.user_deleted,
                        404: openapi.no_username_found
                    })
async def delete_user(
        username: Annotated[str, Query(title="Username", description="Unique user username",
                                       examples=["text_test_test_test1"])],
):
    # connect to the database and execute query
    db.connect()
    # check if user which is to be deleted exist in the database
    db.execute(f"SELECT user_id FROM users WHERE username = '{username}'")
    db_response = db.get_query_results()
    if not db_response:
        raise HTTPException(
            status_code=404,
            detail="No user with a such username"
        )
    # delete user from the database
    db.execute(f"DELETE FROM users WHERE username = '{username}';")
    db.commit()
    return {"message": "User deleted from SQLite"}
