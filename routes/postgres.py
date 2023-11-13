# libraries imports
from fastapi import APIRouter, Header, HTTPException, Query, Body, Path
from typing import Annotated, List
import psycopg2.errors

# packages imports
from models import user, openapi, querry_db, http_custom_error
from SQL_engines.PostgreSQL import PostgreSQL
from config import *


# ### variables ###
psql_router = APIRouter(
    prefix="/psql",
    tags=["PostgreSQL"]
)
# database instance
db = PostgreSQL()


# ### endpoints ###
@psql_router.get("/user/validate", description="Validates whether user exists in PostgreSQL",
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
    # connect to the database
    try:
        db.connect(True)
    except Exception:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    # execute query, fetch response and close connection
    db.execute(f"SELECT * FROM users WHERE username = '{user_username}'")
    db_response = db.get_query_results()
    db.commit()
    # check if user with such username exists
    # return response accordingly
    if not db_response:
        return user.UserExistsRes(exist=False)
    else:
        return user.UserExistsRes(exist=True, password_hashed=db_response[0]["password_hashed"])


@psql_router.get("/users", description="Returns all the information stored about users or specified user",
                 response_description="Returns information retrieved from the database", status_code=200,
                 responses={
                      404: openapi.no_username_found,
                      500: openapi.cannot_connect_to_db
                 })
async def get_user_info(
        username: Annotated[str | None, Query(title="Username",
                                              description="Username by which you can retrieve its info from database")]
        = None) -> user.GetUserInfoRes | List[user.GetUserInfoRes]:

    # connect to the database
    try:
        db.connect(True)
    except Exception:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )

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
            users.append(user.GetUserInfoRes(
                user_id=user_db["user_id"], username=user_db["username"], is_admin=user_db["is_admin"],
                creation_date=user_db["creation_date"]
            ))
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
        # return response
        return user.GetUserInfoRes(
                user_id=db_response[0]["user_id"], username=db_response[0]["username"],
                is_admin=db_response[0]["is_admin"], creation_date=db_response[0]["creation_date"])


@psql_router.post("/users", status_code=201, description="Create new user",
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
    # connect to the database and executes query
    try:
        db.connect(True)
    except Exception:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    try:
        db.execute(f"INSERT INTO users (username, password_hashed) VALUES ('{username}', '{password_hash}');")
    except Exception as e:
        db.commit()
        raise e
    db.commit()
    return {"message": "New user created in PostgreSQL"}


@psql_router.delete("/users", status_code=200, description="Delete user from the database by the username",
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
        db.connect(True)
    except Exception:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail="Can not connect to the database"
        )
    try:
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
    except Exception as e:
        db.commit()
        raise e
    db.commit()
    return {"message": "User deleted from PostgreSQL"}


@psql_router.get("/restart", description="Restarts data Postgres database", status_code=200)
def restart_postgres():

    # connect to the database and executes query
    try:
        db.connect(True)
    except Exception:
        print("[ERROR] Can not connect to the database")
        raise HTTPException(
            status_code=500,
            detail={
                "db_type": "psql",
                "message": "Can not connect to the database"
            }
        )

    try:
        # check if data tables exists and restart it if not
        for table_name in tables_names:
            db.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
            if db.get_query_results()[0]["exists"]:
                # clear table content
                if table_name == "title_basics":
                    db.execute(f"TRUNCATE {table_name} CASCADE;")
                else:
                    db.execute(f"TRUNCATE {table_name};")
            else:
                # create table
                db.execute(tables_create_psql[table_name])
        db.commit()
    except Exception:
        raise HTTPException(
            status_code=500,
            detail={
                "db_type": "psql",
                "message": "Postgres database reset failed"
            }
        )

    return {"message": "Postgres database data set has been reset"}


@psql_router.post("/data", description="Insert data to the PostgreSQL", status_code=201)
async def insert(
    title_basics: Annotated[querry_db.InsertTitleBasic | None, Body()] = None,
    name_basics: Annotated[querry_db.InsertNameBasic | None, Body()] = None,
    title_episode: Annotated[querry_db.InsertTitleEpisode | None, Body()] = None,
):
    # if none data has been provided, rais an error
    if title_basics is None and name_basics is None and title_episode is None:
        raise http_custom_error.lack_of_data

    # check which data has been provided
    try:

        db.connect(True)
        # insert data if provided

        if title_basics is not None:
            db.execute(
                tables_insert_psql["title_basics"].format(
                    tconst=title_basics.tconst, titleType=title_basics.titleType,
                    primaryTitle=title_basics.primaryTitle, originalTitle=title_basics.originalTitle,
                    isAdult=int(title_basics.isAdult), startYear=int(title_basics.startYear),
                    endYear=int(title_basics.endYear), runtimeMinutes=int(title_basics.runtimeMinutes),
                    genres=title_basics.genres
                )
            )

        if name_basics is not None:
            db.execute(
                tables_insert_psql["name_basics"].format(
                    nconst=name_basics.nconst, primaryName=name_basics.primaryName,
                    birthYear=int(name_basics.birthYear), deathYear=int(name_basics.deathYear),
                    primaryProfession=name_basics.primaryProfession.split(","),
                    knownForTitles=name_basics.knownForTitles.split(",")
                )
            )

        if title_episode is not None:
            db.execute(
                tables_insert_psql["title_episode"].format(
                    tconst=title_episode.tconst, parentTconst=title_episode.parentTconst,
                    seasonNumber=int(title_episode.seasonNumber), episodeNumber=int(title_episode.episodeNumber)
                )
            )

        db.commit()
    # syntax error handling
    except psycopg2.errors.SyntaxError as e:
        print("[ERROR] There has been a syntax error while inserting record into db")
        db.commit()
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Invalid SQL syntax while inserting into database.",
                "error_detail": str(e)
            })
    # unique record violation
    except psycopg2.errors.UniqueViolation:
        print("[ERROR] There is already record with such id in the database")
        db.commit()
        raise http_custom_error.record_duplicated
    # cannot connect to db
    except psycopg2.errors.ConnectionException:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db

    return {"message": "Record has been inserted successfully."}


@psql_router.delete("/data", status_code=200, description="Deletes resource from postgres")
async def delete_data_postgres(
        table_name: Annotated[str, Query(title="Table name", examples=["title_basics"])],
        record_id: Annotated[str, Query(title="Username", examples=["tt0000004"])]
):
    # connect to the database
    try:
        # execute query
        db.connect(True)
        indicator = "nconst" if table_name == "name_basics" else "tconst"
        # check if record exists in database
        db.execute(f"SELECT 1 FROM {table_name} WHERE {indicator} = '{record_id}';")

        if db.get_query_results():
            db.execute(f"DELETE FROM {table_name} WHERE {indicator} = '{record_id}';")
            db.commit()
        else:
            db.commit()
            raise HTTPException(
                status_code=404,
                detail="There is no such record in the database"
            )

    # syntax error handling
    except psycopg2.errors.SyntaxError as e:
        print("[ERROR] There has been a syntax error while inserting record into db")
        db.commit()
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Invalid SQL syntax while inserting into database.",
                "error_detail": str(e)
            })
    # cannot connect to db
    except psycopg2.errors.ConnectionException:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db

    return {"message": "Record deleted"}


@psql_router.get("/data", status_code=200, description="Get all resources from postgres")
async def get_all_data_postgres(
):
    # connect to the database
    try:
        data = {}
        # execute query
        db.connect(True)
        for table in tables_names:
            db.execute(f"SELECT * FROM {table};")
            data[table] = db.get_query_results()
        db.commit()

    # cannot connect to db
    except psycopg2.errors.ConnectionException:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db

    return {"data": {
        "title_basics": data["title_basics"],
        "title_episodes": data["title_episodes"],
        "name_basics": data["name_basics"]
    }}


@psql_router.get("/data/{table_name}", status_code=200, description="Get table resource from postgres")
async def get_table_data_postgres(
    table_name: Annotated[str, Path(title="Table name", description="Name of table you want to perform operation on",
                                    example="title_basics")]
):
    # connect to the database
    try:
        # execute query
        db.connect(True)
        db.execute(f"SELECT * FROM {table_name};")
        data = db.get_query_results()
        db.commit()

    # cannot connect to db
    except psycopg2.errors.ConnectionException:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db
    return {"data": data}


@psql_router.get("/data/{table_name}/{record_id}", status_code=200, description="Get record resource from postgres")
async def get_record_data_postgres(
    table_name: Annotated[str, Path(title="Table name", description="Name of table you want to perform operation on",
                                    example="title_basics")],
    record_id: Annotated[str, Path(title="Record identifier", description="Identifies specific record in table",
                                   example="tt0000004")]
):
    # connect to the database
    try:
        # execute query
        db.connect(True)
        indicator = "nconst" if table_name == "name_basics" else "tconst"
        db.execute(f"SELECT * FROM {table_name} WHERE {indicator} = '{record_id}';")
        data = db.get_query_results()
        db.commit()
        if not data:
            raise http_custom_error.no_such_record

    # cannot connect to db
    except psycopg2.errors.ConnectionException:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db

    return {"data": data[0]}


@psql_router.patch("/data/{table_name}/{record_id}", status_code=204, description="Update record in postgres")
async def update_record_postgres(
        table_name: Annotated[
            str, Path(title="Table name", description="Name of table you want to perform operation on",
                      example="title_basics")],
        record_id: Annotated[str, Path(title="Record identifier", description="Identifies specific record in table",
                                       example="tt0000004")],
        data: Annotated[dict, Body()]
):

    # prepare data to insert
    fields_to_update = ""
    for field in data:
        fields_to_update = fields_to_update + f"{field} = '{data[field]}', "
    # deletes ',' from last insert
    fields_to_update = fields_to_update[:-2]
    # connect to the database
    try:
        # execute query
        db.connect(True)
        indicator = "nconst" if table_name == "name_basics" else "tconst"
        db.execute(f"UPDATE {table_name} SET {fields_to_update} WHERE {indicator} = '{record_id}';")
        db.commit()

    # cannot connect to db
    except psycopg2.errors.ConnectionException:
        print("[ERROR] Can not connect to the database")
        raise http_custom_error.cannot_connect_to_db
