# libraries imports
from fastapi import APIRouter, Header, HTTPException, Query, Body, Path
from typing import Annotated, List
from pymongo import MongoClient
from datetime import datetime
from pymongo.errors import ServerSelectionTimeoutError

# packages imports
from models import user, openapi, querry_db, http_custom_error
from config import *


# ### variables ###
mdb_router = APIRouter(
    prefix="/mdb",
    tags=["MongoDB"]
)

try:
    # mongo client
    client = MongoClient(MDB_HOST, MDB_PORT)
    # mongo database
    db = client[MDB_DB]
    # define collection
    users = db["users"]
    title_basics_collection = db["title_basics"]
    name_basics_collection = db["name_basics"]
    title_episodes_collection = db["title_episodes"]
except ServerSelectionTimeoutError as e:
    print("[ERROR] Can not connect to the database")
    raise e


# ### endpoints ###
@mdb_router.get("/user/validate", description="Validates whether user exists in MongoDB",
                response_description="Returns flag and hashed_password if user exists", status_code=200,
                responses={
                  500: openapi.cannot_connect_to_db
                })
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


@mdb_router.get("/users", description="Returns all the information stored about users or specified user",
                response_description="Returns information retrieved from the database", status_code=200,
                responses={
                  404: openapi.no_username_found,
                  500: openapi.cannot_connect_to_db
                })
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


@mdb_router.post("/users", status_code=201, description="Create new user",
                 responses={
                    201: openapi.new_user_created,
                    500: openapi.cannot_connect_to_db
                 })
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


@mdb_router.delete("/users", status_code=200, description="Delete user from the database by the username",
                   responses={
                        200: openapi.user_deleted,
                        404: openapi.no_username_found,
                        500: openapi.cannot_connect_to_db
                   })
async def delete_user(
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


@mdb_router.get("/restart", description="Restarts data MongoDB database", status_code=200)
def restart_mongo():
    # connect to the database and executes query
    try:
        # restart all collections
        for table_name in tables_names:
            db[table_name].delete_many({})
    except ServerSelectionTimeoutError:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail={
                "db_type": "mdb",
                "message": "Can not connect to the database"
            }
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                "db_type": "mdb",
                "message": "MongoDB database reset failed"
            }
        )

    return {"message": "MongoDB database data set has been reset"}


@mdb_router.post("/data", description="Insert data MongoDB database", status_code=201)
async def insert_mongo(
    title_basics: Annotated[querry_db.InsertTitleBasic | None, Body()] = None,
    name_basics: Annotated[querry_db.InsertNameBasic | None, Body()] = None,
    title_episode: Annotated[querry_db.InsertTitleEpisode | None, Body()] = None
):
    # no data provided flag
    no_data = True

    # check which data has been provided
    try:

        # insert data if provided
        if title_basics is not None:
            no_data = False
            title_basics_collection.insert_one({
                "tconst": title_basics.tconst, "titleType": title_basics.titleType,
                "primaryTitle": title_basics.primaryTitle, "originalTitle": title_basics.originalTitle,
                "isAdult": int(title_basics.isAdult), "startYear": int(title_basics.startYear),
                "endYear": int(title_basics.endYear), "runtimeMinutes": int(title_basics.runtimeMinutes),
                "genres": title_basics.genres
            })

        if name_basics is not None:
            no_data = False
            name_basics_collection.insert_one({
                "nconst": name_basics.nconst, "primaryName": name_basics.primaryName,
                "birthYear": int(name_basics.birthYear), "deathYear": int(name_basics.deathYear),
                "primaryProfession": name_basics.primaryProfession, "knownForTitles": name_basics.knownForTitles
            })

        if title_episode is not None:
            no_data = False
            title_episodes_collection.insert_one({
                "tconst": title_episode.tconst, "parentTconst": title_episode.parentTconst,
                "seasonNumber": int(title_episode.seasonNumber), "episodeNumber": int(title_episode.episodeNumber)
            })

    except ServerSelectionTimeoutError:
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


@mdb_router.delete("/data", status_code=200, description="Deletes resource from mongodb")
async def delete_data_mongo(
        table_name: Annotated[str, Query(title="Table name", examples=["title_basics"])],
        record_id: Annotated[str, Query(title="Username", examples=["tt0000004"])]
):

    # connect to the database and execute query
    try:
        indicator = "nconst" if table_name == "name_basics" else "tconst"
        if db[str(table_name)].find_one({indicator: record_id}):
            db[str(table_name)].delete_one({indicator: record_id})
        else:
            raise HTTPException(
                status_code=404,
                detail="There is no such record in the database"
            )
    except ServerSelectionTimeoutError:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    return {"message": "Record deleted"}


@mdb_router.get("/data", status_code=200, description="Get all resources from mongo")
async def get_all_data_mongo(
):
    data = {}
    # connect to the database
    try:
        for table_name in tables_names:
            data[table_name] = list(db[table_name].find({}, {'_id': 0}))

    # cannot connect to db
    except ServerSelectionTimeoutError:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db

    return {"data": {
        "title_basics": data["title_basics"],
        "title_episodes": data["title_episodes"],
        "name_basics": data["name_basics"]
    }}


@mdb_router.get("/data/{table_name}", status_code=200, description="Get table resource from mongo")
async def get_table_data_mongo(
    table_name: Annotated[str, Path(title="Table name", description="Name of table you want to perform operation on",
                                    example="title_basics")]
):
    # connect to the database
    try:
        # execute query
        data = list(db[table_name].find({}, {'_id': 0}))

    # cannot connect to db
    except ServerSelectionTimeoutError:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db

    return {"data": data}


@mdb_router.get("/data/{table_name}/{record_id}", status_code=200, description="Get record resource from mongo")
async def get_record_data_mongo(
    table_name: Annotated[str, Path(title="Table name", description="Name of table you want to perform operation on",
                                    example="title_basics")],
    record_id: Annotated[str, Path(title="Record identifier", description="Identifies specific record in table",
                                   example="tt0000004")]
):
    # connect to the database
    try:
        # execute query
        indicator = "nconst" if table_name == "name_basics" else "tconst"
        # execute query
        data = db[table_name].find_one({indicator: record_id}, {'_id': 0})
        if not data:
            raise http_custom_error.no_such_record

    # cannot connect to db
    except ServerSelectionTimeoutError:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db

    return {"data": data}


@mdb_router.patch("/data/{table_name}/{record_id}", status_code=204, description="Update record in mongo")
async def update_record_mongo(
        table_name: Annotated[
            str, Path(title="Table name", description="Name of table you want to perform operation on",
                      example="title_basics")],
        record_id: Annotated[str, Path(title="Record identifier", description="Identifies specific record in table",
                                       example="tt0000004")],
        data: Annotated[dict, Body()]
):

    # prepare data to insert
    fields_to_update = {"$set": data}

    # connect to the database
    try:
        # execute query
        indicator = "nconst" if table_name == "name_basics" else "tconst"
        db[table_name].update_one({indicator: record_id}, fields_to_update)

    # cannot connect to db
    except ServerSelectionTimeoutError:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db
