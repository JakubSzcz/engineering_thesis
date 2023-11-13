# library imports
from fastapi import APIRouter, Header, HTTPException, Body, Query
from typing import Annotated
import httpx
import asyncio
import re

# packages imports
from utilities import functions as fun
from models import querry_db, user
from config import *


# ### variables ###
proc_router = APIRouter(
    prefix="/proc",
    tags=["Process"],
)


# ### functions ###


# ### endpoints ###
@proc_router.get("/db_restart", description="Endpoints for databases restart operation", status_code=200)
async def restart_db(
        redis: Annotated[bool, Header(title="Redis Flag", description="Indicates to restart Redis database",
                                      example="True")],
        postgres: Annotated[bool, Header(title="Postgres Flag", description="Indicates to restart PostgreSQL"
                                                                            " database", example="True")],
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
            detail=f"Restart of this database failed: {db_failed}"
        )
    else:
        return {"message": f"Restart of this databases has finished with a success: {db_to_send}"}


@proc_router.post("/data", description="Insert data to the provided database", status_code=201)
async def insert(
    db_type: Annotated[str, Header(title="Database type", description="Database type destination", example="psql")],
    correlation_id: Annotated[str, Header(title="Request correlation identifier",
                                          description="Identifies every unique data insertion request",
                                          example="psql")],
    title_basics: Annotated[querry_db.InsertTitleBasic | None, Body()] = None,
    name_basics: Annotated[querry_db.InsertNameBasic | None, Body()] = None,
    title_episode: Annotated[querry_db.InsertTitleEpisode | None, Body()] = None,
):
    # validate db_type
    fun.validate_db_type(db_type)

    # ensure body is correct
    if title_basics is None and name_basics is None and title_episode is None:
        raise HTTPException(
            status_code=400,
            detail="Required body content not provided."
        )

    data = {}
    if title_basics is not None:
        data["title_basics"] = title_basics.model_dump()

    if name_basics is not None:
        data["name_basics"] = name_basics.model_dump()

    if title_episode is not None:
        data["title_episode"] = title_episode.model_dump()

    # send request
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=fun.compose_url(SYS_IP, SYS_PORT) + f"/{db_type}/data",
            json=data
        )

    # handel responses
    if response.status_code == 201:
        return {"correlation_id": correlation_id, "status": "inserted",
                "db_source": db_type, "message": "Record successfully inserted."}
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"]
        )


@proc_router.delete("/data")
async def delete_data(
        db_type: Annotated[str, Header(title="Database type", description="Database type destination", example="psql")],
        table_name: Annotated[str, Query(title="Table name", examples=["title_basics"])],
        record_id: Annotated[str, Query(title="Username", examples=["tt0000004"])]
):
    # validate db_type
    fun.validate_db_type(db_type)
    # validate table name
    fun.validate_table_name(table_name)

    # pre validate record_id
    if not re.match(r"^[tnm][tnm]\d+$", str(record_id)):
        raise HTTPException(
            status_code=400,
            detail="Invalid record_id format. Record id should looks like {t/n/m}{t/n/m}XXXXX, X- digit"
        )

    # route request to the appropriate sys endpoint
    try:
        # send request to the sys_api
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                url=fun.compose_url(SYS_IP, SYS_PORT) + f"/{db_type}/data?table_name={table_name}&record_id={record_id}"
            )

        # handle responses
        if response.status_code == 200:
            return {"message": "Record deleted"}
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["detail"]
            )
    # handel connection error
    except httpx.ConnectError:
        raise HTTPException(
            status_code=500,
            detail="Cannot connect to the sys_api"
        )


@proc_router.get("/data")
async def get_data(
        db_type: Annotated[str, Header(title="Database type", description="Database type destination", example="psql")],
        filters: Annotated[bool, Query(title="Filters indicator flag", examples=["True"])],
        table_name: Annotated[str | None, Query(title="Table name", examples=["title_basics"])] = None,
        record_id: Annotated[str | None, Query(title="Username", examples=["tt0000004"])] = None
):
    # validate db_type
    fun.validate_db_type(db_type)
    # route request to the appropriate sys endpoint
    try:
        # retrieved filters
        if filters:
            # validate table name
            fun.validate_table_name(table_name)
            # record_id handling
            if record_id is not None:
                # pre validate record_id
                if not re.match(r"^[tnm][tnm]\d+$", str(record_id)):
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid record_id format. Record id should looks like {t/n/m}{t/n/m}XXXXX, X- digit"
                    )

                # send request to the sys_api about record_id related resource
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        url=fun.compose_url(SYS_IP, SYS_PORT) + f"/{db_type}/data/{table_name}/{record_id}"
                    )
            # table_name handling
            else:
                # send request to the sys_api about table related resource
                async with httpx.AsyncClient() as client:
                    response = await client.get(
                        url=fun.compose_url(SYS_IP, SYS_PORT) + f"/{db_type}/data/{table_name}"
                    )
        # all resource handling
        else:
            # send request to the sys_api about all resources
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=fun.compose_url(SYS_IP, SYS_PORT) + f"/{db_type}/data"
                )

    # handel connection error
    except httpx.ConnectError:
        raise HTTPException(
            status_code=500,
            detail="Cannot connect to the sys_api"
        )
    # handle responses
    if response.status_code == 200 and not filters:
        return {"data": {
            "title_basics": response.json()["data"]["title_basics"],
            "title_episodes": response.json()["data"]["title_episodes"],
            "name_basics": response.json()["data"]["name_basics"]
        }}
    elif response.status_code == 200 and filters:
        return {"data": response.json()["data"]}
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.json()["detail"]
        )

