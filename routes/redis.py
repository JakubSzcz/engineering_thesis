# libraries imports
from datetime import datetime
import redis
from fastapi import APIRouter, Header, HTTPException, Query, Body, Path
from typing import Annotated, List
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query as redisQuery
from redis.commands.search.aggregation import AggregateRequest
import random
import re

# packages imports
from models import user, openapi, querry_db, http_custom_error
from config import *


# ### variables ###
redis_router = APIRouter(
    prefix="/redis",
    tags=["Redis"]
)
# create redis instance
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
# dict with indexes
indexes = {}


# ### functions ###
# ensure that certain index exists, if not, creates one
def create_indexes(index_name: str):
    # try to retrieve index
    try:
        index = r.ft("idx:" + index_name)
        # if index exists
        index.info()
        return index
    # no connection with the database
    except redis.exceptions.ConnectionError as e:
        print("[ERROR] Can not connect to the Redis database")
        # raise e # TODO uncomment on testing
    except redis.exceptions.ResponseError:
        # if no index exists, create new one
        schema = indexes_create_schema[index_name]["schema"]
        r.ft("idx:" + index_name).create_index(schema, definition=IndexDefinition(
            index_type=IndexType.HASH, prefix=[indexes_create_schema[index_name]["prefix"]]))
        print("[INFO] New index created")
        return r.ft("idx:" + index_name)


# change list to the valid dict
def redis_list_to_dict(data_list, table: str | None = None):

    if table is not None:
        data = []
        for record in data_list:
            record_to_add = {}
            for i in range(0, len(record), 2):
                if re.match(r'^-?\d+$', str(record[i + 1])):
                    record_to_add[record[i]] = int(record[i + 1])
                else:
                    record_to_add[record[i]] = record[i + 1]
            data.append(record_to_add)
    else:
        data = {}
        # change list od list result into list of dict
        for table_name in tables_names:
            data[table_name] = []
            for record in data_list[table_name]:
                record_to_add = {}
                for i in range(0, len(record), 2):
                    if re.match(r'^-?\d+$', str(record[i + 1])):
                        record_to_add[record[i]] = int(record[i + 1])
                    else:
                        record_to_add[record[i]] = record[i + 1]
                data[table_name].append(record_to_add)

    return data


# create indexes
indexes["users"] = create_indexes("users")
indexes["title_basics"] = create_indexes("title_basics")
indexes["name_basics"] = create_indexes("name_basics")
indexes["title_episodes"] = create_indexes("title_episodes")


# ### endpoints ###
@redis_router.get("/user/validate", description="Validates whether user exists in Redis",
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
    users = indexes["users"]
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


@redis_router.get("/users", description="Returns all the information stored about users or specified user",
                  response_description="Returns information retrieved from the database", status_code=200,
                  responses={
                      404: openapi.no_username_found,
                      500: openapi.cannot_connect_to_db
                  })
async def get_user_info(
        username: Annotated[str | None, Query(title="Username",
                                              description="Username by which you can retrieve its info from database")]
        = None) -> user.GetUserInfoRes | List[user.GetUserInfoRes]:

    users = indexes["users"]
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


@redis_router.post("/users", status_code=201, description="Create new user",
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


@redis_router.delete("/users", status_code=200, description="Delete user from the database by the username",
                     responses={
                        200: openapi.user_deleted,
                        404: openapi.no_username_found,
                        500: openapi.cannot_connect_to_db
                     })
async def delete_user(
        username: Annotated[str, Query(title="Username", description="Unique user username",
                                       examples=["text_test_test_test1"])],
):

    users = indexes["users"]
    # connect to the database and execute query
    try:
        db_response = users.search(redisQuery(f"@username:{username}"))
        if len(db_response.docs) != 0:
            r.delete(str(db_response.docs[0]["id"]))
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


@redis_router.get("/restart", description="Restarts data Redis database", status_code=200)
def restart_redis():
    # connect to the database and executes query
    try:
        # deletes all from database
        r.flushall()
        # creates data indexes
        for index_name in tables_names:
            indexes[index_name] = create_indexes(index_name)
        # create users index
        indexes["users"] = create_indexes("users")
    except redis.exceptions.ConnectionError:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail={
                "db_type": "redis",
                "message": "Can not connect to the database"
            }
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                "db_type": "redis",
                "message": "Redis database reset failed"
            }
        )

    return {"message": "Redis database data set has been reset"}


@redis_router.post("/data", description="Insert data Postgres database", status_code=201)
async def insert_redis(
    title_basics: Annotated[querry_db.InsertTitleBasic | None, Body()] = None,
    name_basics: Annotated[querry_db.InsertNameBasic | None, Body()] = None,
    title_episode: Annotated[querry_db.InsertTitleEpisode | None, Body()] = None
):
    # no data provided flag
    no_data = True

    # check which data has been provided
    try:

        # insert data if provided
        if title_basics:
            no_data = False
            # check if data already exists
            db_response = indexes["title_basics"].search(redisQuery(f"@tconst:{title_basics.tconst}"))
            if len(db_response.docs) == 0:
                # insert data
                r.hset(name=("title_basics:" + str(int(datetime.utcnow().timestamp()) +
                                             random.randint(1,9999))), mapping={
                       "tconst": title_basics.tconst, "titleType": title_basics.titleType,
                       "primaryTitle": title_basics.primaryTitle,
                       "originalTitle": title_basics.originalTitle, "isAdult": int(title_basics.isAdult),
                       "startYear": int(title_basics.startYear), "endYear": int(title_basics.endYear),
                       "runtimeMinutes": int(title_basics.runtimeMinutes), "genres": title_basics.genres
                    })
            else:
                raise http_custom_error.record_duplicated

        if name_basics:
            no_data = False
            # check if data already exists
            db_response = indexes["name_basics"].search(redisQuery(f"@nconst:{name_basics.nconst}"))
            if len(db_response.docs) == 0:
                # insert data
                r.hset(name=("name_basics:" + str(int(datetime.utcnow().timestamp()) +
                                                  random.randint(1,9999))), mapping={
                        "tconst": name_basics.nconst, "primaryName": name_basics.primaryName,
                        "birthYear": int(name_basics.birthYear), "deathYear": int(name_basics.deathYear),
                        "primaryProfession": name_basics.primaryProfession, "knownForTitles": name_basics.knownForTitles
                })
            else:
                raise http_custom_error.record_duplicated

        if title_episode:
            no_data = False
            # check if data already exists
            db_response = indexes["title_episodes"].search(redisQuery(f"@tconst:{title_episode.tconst}"))
            if len(db_response.docs) == 0:
                # insert data
                r.hset(name=("title_episodes:" + str(int(datetime.utcnow().timestamp()) +
                                                     random.randint(1,9999))), mapping={
                        "tconst": title_episode.tconst, "parentTconst": title_episode.parentTconst,
                        "seasonNumber": int(title_episode.seasonNumber), "episodeNumber": int(title_episode.episodeNumber)
                })
            else:
                raise http_custom_error.record_duplicated
    except redis.exceptions.ConnectionError:
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

    return {"db_type": "redis", "message":  "Record has been inserted successfully."}


@redis_router.delete("/data", status_code=200, description="Deletes resource from redis")
async def delete_data_redis(
        table_name: Annotated[str, Query(title="Table name", examples=["title_basics"])],
        record_id: Annotated[str, Query(title="Username", examples=["tt0000004"])]
):
    # connect to index
    index = indexes[table_name]

    # connect to the database and execute query
    try:
        indicator = "nconst" if table_name == "name_basics" else "tconst"
        db_response = index.search(redisQuery(f"@{indicator}:{record_id}"))
        if len(db_response.docs) != 0:
            r.delete(str(db_response.docs[0]["id"]))
        else:
            raise HTTPException(
                status_code=404,
                detail="There is no such record in the database"
            )
    except redis.exceptions.ConnectionError:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    return {"message": "Record deleted"}


@redis_router.get("/data", status_code=200, description="Get all resources from redis")
async def get_all_data_redis(
):
    # connect to the database
    try:
        data_list = {}
        """
        for table_name in tables_names:
            #query = redisQuery("*")
            #query._num = indexes[table_name].search("*").total
            #data[table_name] = indexes[table_name].search(query).docs
        """
        for table_name in tables_names:
            data_list[table_name] = (indexes[table_name].aggregate(AggregateRequest("*").load().group_by(
                querry_db.redis_models_fields_tuple[table_name])).rows)

        data = redis_list_to_dict(data_list)

    except redis.exceptions.ConnectionError:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db

    return {"data": {
        "title_basics": data["title_basics"],
        "title_episodes": data["title_episodes"],
        "name_basics": data["name_basics"]
    }}


@redis_router.get("/data/{table_name}", status_code=200, description="Get table resource from redis")
async def get_table_data_redis(
    table_name: Annotated[str, Path(title="Table name", description="Name of table you want to perform operation on",
                                    example="title_basics")]
):
    # connect to the database
    try:

        data_list = (indexes[table_name].aggregate(AggregateRequest("*").load().group_by(
                    querry_db.redis_models_fields_tuple[table_name])).rows)

        data = redis_list_to_dict(data_list, table_name)

    except redis.exceptions.ConnectionError:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db

    return {"data": data}


@redis_router.get("/data/{table_name}/{record_id}", status_code=200, description="Get record resource from redis")
async def get_record_data_redis(
    table_name: Annotated[str, Path(title="Table name", description="Name of table you want to perform operation on",
                                    example="title_basics")],
    record_id: Annotated[str, Path(title="Record identifier", description="Identifies specific record in table",
                                   example="tt0000004")]
):
    # connect to the database
    try:

        data_list = (indexes[table_name].aggregate(AggregateRequest(f"@tconst:{record_id}").load().group_by(
            querry_db.redis_models_fields_tuple[table_name])).rows)

        if not data_list:
            raise http_custom_error.no_such_record

        data = {}
        record = data_list[0]
        for i in range(0, len(record), 2):
            if re.match(r'^-?\d+$', str(record[i + 1])):
                data[record[i]] = int(record[i + 1])
            else:
                data[record[i]] = record[i + 1]

    except redis.exceptions.ConnectionError:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db

    return {"data": data}
