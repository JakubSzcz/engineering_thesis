# library imports
from fastapi import APIRouter, Header, HTTPException
from typing import Annotated
import asyncio

# packages imports
from utilities import functions as fun


# ### variables ###
proc_router = APIRouter(
    prefix="/proc",
    tags=["proc"],
)


# ### functions ###


# ### endpoints ###
@proc_router.get("/db_restart", description="Endpoints for databases restart operation", status_code=200)
async def restart_db(
        redis: Annotated[bool, Header(title="Redis Flag", description="Indicates to restart Redis database",
                                      example="True")],
        postgres: Annotated[bool, Header(title="Postgres Flag", description="Indicates to restart PostgreSQL"
                                                                                   " database",example="True")],
        mongo: Annotated[bool, Header(title="Mongo Flag", description="Indicates to restart MongoDB database",
                                      example="True")],
        sqlite: Annotated[bool, Header(title="SQLite Flag", description="Indicates to restart SQLite database",
                                      example="True")]
):
    # verify which db_type has been provided
    db_to_send = []
    if redis:
        db_to_send.append("redis")

    if postgres:
        db_to_send.append("psql")

    if mongo:
        db_to_send.append("mdb")

    if sqlite:
        db_to_send.append("sqlite")

    if len(db_to_send) == 0:
        raise HTTPException(
            status_code=500,
            detail="No database header provided"
        )

    # collect parallel responses
    responses = await asyncio.gather(*(fun.send_async_request_restart_db(db_name) for db_name in db_to_send))

    # check whether responses were 200
    db_failed = []
    for response in responses:
        if response.status_code != 200:
            db_failed.append(response.json()["detail"]["db_type"])

    if len(db_failed) > 0:
        raise HTTPException(
            status_code=500,
            detail="Restart of this database failed: " + str(db_failed)
        )
    else:
        return {"message": "Restart of this databases has finished with a success: " + str(db_to_send)}



