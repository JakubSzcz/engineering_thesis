# libraries imports
import sqlite3

from fastapi import APIRouter, Header, HTTPException, Query, Body
from typing import Annotated, List
from datetime import datetime
import os


# packages imports
from models import user, openapi, querry_db, http_custom_error
from config import *
from SQL_engines.SQLite import SQLite

# ### variables ###
sqli_router = APIRouter(
    prefix="/sqlite",
    tags=["SQLite3"]
)
# connecting to the database file and create tables
db = SQLite()
if "sqlitedb.db" not in os.listdir("./SQL_engines"):
    db.connect()
    # create users database
    db.execute(tables_create_sqli["users"])
    # create title_basics database
    db.execute(tables_create_sqli["title_basics"])
    # create name_basics database
    db.execute(tables_create_sqli["name_basics"])
    # create title_episodes database
    db.execute(tables_create_sqli["title_episodes"])
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


@sqli_router.get("/restart", description="Restarts data SQLite database", status_code=200)
def restart_sqlite():

    # connect to the database and executes query
    try:
        db.connect()
    except Exception:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail={
                "db_type": "sqlite",
                "message": "Can not connect to the database"
            }
        )
    # check if data tables exists and restart it if not
    try:
        for table_name in tables_names:
            db.execute(f"DELETE FROM {table_name};")
        db.commit()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                "db_type": "sqlite",
                "message": "SQLite database reset failed"
            }
        )

    return {"message": "SQLite database data set has been reset"}


@sqli_router.post("/insert", description="Insert data SQLite database", status_code=201)
async def insert_sqlite(
    title_basics: Annotated[querry_db.InsertTitleBasic | None, Body()] = None,
    name_basics: Annotated[querry_db.InsertNameBasic | None, Body()] = None,
    title_episode: Annotated[querry_db.InsertTitleEpisode | None, Body()] = None
):
    # no data provided flag
    no_data = True

    # check which data has been provided
    try:
        db.connect()
        # insert data if provided
        if title_basics:
            no_data = False
            db.execute(
                tables_insert_sqli["title_basics"].format(
                    tconst=title_basics.tconst, titleType=title_basics.titleType,
                    primaryTitle=title_basics.primaryTitle, originalTitle=title_basics.originalTitle,
                    isAdult=int(title_basics.isAdult), startYear=int(title_basics.startYear),
                    endYear=int(title_basics.endYear), runtimeMinutes=int(title_basics.runtimeMinutes),
                    genres=title_basics.genres
                )
            )

        if name_basics:
            no_data = False
            db.execute(
                tables_insert_sqli["name_basics"].format(
                    nconst=name_basics.nconst, primaryName=name_basics.primaryName,
                    birthYear=int(name_basics.birthYear), deathYear=int(name_basics.deathYear),
                    primaryProfession=name_basics.primaryProfession, knownForTitles=name_basics.knownForTitles
                )
            )

        if title_episode:
            no_data = False
            db.execute(
                tables_insert_sqli["title_episodes"].format(
                    tconst=title_episode.tconst, parentTconst=title_episode.parentTconst,
                    seasonNumber=int(title_episode.seasonNumber), episodeNumber=int(title_episode.episodeNumber)
                )
            )

        db.commit()

    except sqlite3.Error as er:
        if er.sqlite_errorcode == 1555:
            print("[ERROR] There is already record with such id in the database")
            db.commit()
            raise http_custom_error.record_duplicated
        else:
            print("[ERROR] Can not connect to the database")
            raise HTTPException(
                status_code=500,
                detail="Can not connect to the database"
            )

    # if none data has been provided, rais an error
    if no_data:
        raise HTTPException(
            status_code=422,
            detail="None of the data to be inserted has been provided"
        )

    return {"message":  "Record has been inserted successfully."}
