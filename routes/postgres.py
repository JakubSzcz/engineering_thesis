# libraries imports
from fastapi import APIRouter, Header, HTTPException, Query, Body
from typing import Annotated, List

# packages imports
from models import user
from postgres_db.PostgreSQL import PostgreSQL


# ### variables ###
psql_router = APIRouter(
    prefix="/psql",
    tags=["PostgreSQL"]
)
# database instance
db = PostgreSQL()


# ### endpoints ###
@psql_router.get("/user/validate", description="Validates whether user exists in PostgreSQL",
                 response_description="Returns flag and hashed_password if user exists", status_code=200)
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


@psql_router.get("/user", description="Returns all the information stored about users or specified user",
                 response_description="Returns information retrieved from the database", status_code=200)
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


@psql_router.post("/user", status_code=201, description="Create new user")
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


@psql_router.delete("/user", status_code=200, description="Delete user from the database by the username")
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
