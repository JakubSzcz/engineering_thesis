from fastapi import APIRouter, Header, HTTPException
from typing import Annotated

from models import user
from postgres_db.PostgreSQL import PostgreSQL


# ### variables ###
psql_router = APIRouter(
    prefix="/psql",
    tags=["PostgreSQL"],
)
# database instance
db = PostgreSQL()


# ### endpoints ###
# get user info from db
@psql_router.get("/user", description="Validates whether user exists and password is correct")
async def get_user_info(
        user_username: Annotated[str, Header(example="abcdefgh12345678", min_length=16, max_length=32,
                                             title="Client username", description="Unique char sequence provided by the"
                                                                                  " client in order to"
                                                                                  " identifies users")]
):
    try:
        db.connect(True)
    except Exception:
        print("[ERROR] Can not connect to the database")
        return {"error_msg": "Can not connect to the database"}
    db.execute(f"SELECT * FROM users WHERE username = '{user_username}'")
    db_response = db.get_query_results()
    db.commit()
    # check if user with such username exists
    if not db_response:
        return {"exist": False}
    else:
        return {"exist": True, "password_hashed": db_response[0]["password_hashed"]}
