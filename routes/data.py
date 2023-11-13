# libraries import
from fastapi import APIRouter, Header, HTTPException, Body, exceptions, Path
from typing import Annotated
import httpx
from datetime import datetime

# packages import
from config import *
from models import user, querry_db, openapi
from utilities import functions as fun

# ### variables ###
data_router = APIRouter(
    prefix="/data",
    tags=["Data"],
)

# ### functions ###


# ### endpoints ###
@data_router.post("", description="Inserting data to the desired database engine", status_code=201,
                  response_description="Basic information about the insertion such as database type or insertion time",
                  responses={
                    400: openapi.wrong_db_type_header,
                    422: openapi.non_data_provided,
                    460: openapi.record_duplication,
                    500: openapi.cannot_connect_to_proc_api
                  })
async def insert_data_to_db(
        db_type: Annotated[str, Header(title="Database type", description="Select database you want to retrieve users "
                                                                        "info from: ['redis', 'mdb', 'psql', 'sqlite']",
                                       examples=['redis', 'mdb', 'psql', 'sqlite'])],
        title_basics: Annotated[querry_db.InsertTitleBasic | None, Body()] = None,
        name_basics: Annotated[querry_db.InsertNameBasic | None, Body()] = None,
        title_episode: Annotated[querry_db.InsertTitleEpisode | None, Body()] = None
) -> querry_db.InsertResponses:

    start_time = datetime.utcnow()

    # data to be sent
    data = {}

    if title_basics is not None:
        data["title_basics"] = title_basics.model_dump()
        tb_id = title_basics.tconst
    else:
        tb_id = "none"

    if title_episode is not None:
        data["title_episode"] = title_episode.model_dump()
        te_id = title_episode.tconst
    else:
        te_id = "none"

    if name_basics is not None:
        data["name_basics"] = name_basics.model_dump()
        nb_id = name_basics.nconst
    else:
        nb_id = "none"
    # create correlation id
    correlation_id = fun.create_correlation_id(tb_id, te_id, nb_id)

    try:
        # send request to the proc_api
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=fun.compose_url(PROC_IP, PROC_PORT) + "/proc/data",
                headers=httpx.Headers({
                    "db-type": db_type,
                    "correlation-id": correlation_id
                }),
                json=data
            )

        # handle responses
        if response.status_code == 201:
            return querry_db.InsertResponses(db_type=db_type, correlation_id=correlation_id,
                                             insertion_time=str(datetime.utcnow() - start_time))
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["detail"]
            )
    # handel Validation error
    except exceptions.ResponseValidationError:
        return response.json()

    except httpx.ConnectError:
        raise HTTPException(
            status_code=500,
            detail="Cannot connect to the proc_api"
        )


@data_router.delete("/{table_name}/{record_id}", status_code=200, description="Deleting data from database",
                    response_description="Deletion confirmation")
async def delete_data(
    table_name: Annotated[str, Path(title="Table name", description="Name of table you want to perform operation on",
                                    example="title_basics")],
    record_id: Annotated[str, Path(title="Record identifier", description="Identifies specific record in table",
                                   example="tt0000004")],
    db_type: Annotated[str, Header(title="Database type", description="Select database you want to retrieve users "
                                                                      "info from: ['redis', 'mdb', 'psql', 'sqlite']",
                                   examples=['redis', 'mdb', 'psql', 'sqlite'])],
):

    try:
        # send request to the proc_api
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                url=fun.compose_url(PROC_IP, PROC_PORT) + "/proc/data?table_name=" + str(table_name)
                + "&record_id=" + str(record_id),
                headers=httpx.Headers({
                    "db-type": db_type
                })
            )

        # handle responses
        if response.status_code == 200:
            return querry_db.DeleteResponses(db_type=db_type, table_name=table_name, record_id=record_id)
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["detail"]
            )
    # handel Validation error
    except exceptions.ResponseValidationError:
        return response.json()

    except httpx.ConnectError:
        raise HTTPException(
            status_code=500,
            detail="Cannot connect to the proc_api"
        )


@data_router.get("", status_code=200, description="Get all data from all tables contained in one database",
                    response_description="Database record response")
async def get_all_data(
    db_type: Annotated[str, Header(title="Database type", description="Select database you want to retrieve users "
                                                                      "info from: ['redis', 'mdb', 'psql', 'sqlite']",
                                   examples=['redis', 'mdb', 'psql', 'sqlite'])]
) -> querry_db.GetResponses:

    try:
        # send request to the proc_api
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=fun.compose_url(PROC_IP, PROC_PORT) + "/proc/data",
                headers=httpx.Headers({
                    "db-type": db_type
                }),
                params=httpx.QueryParams({
                    "filters": "False"
                })
            )

        # handle responses
        if response.status_code == 200:
            return querry_db.GetResponses(
                db_type=db_type,
                title_basics=response.json()["data"]["title_basics"],
                title_episodes=response.json()["data"]["title_episodes"],
                name_basics=response.json()["data"]["name_basics"]
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["detail"]
            )

    # handel Validation error
    except exceptions.ResponseValidationError:
        return response.json()

    except httpx.ConnectError:
        raise HTTPException(
            status_code=500,
            detail="Cannot connect to the proc_api"
        )


@data_router.get("/{table_name}", status_code=200, description="Get data from specified table from the database",
                    response_description="Database record response")
async def get_table_data(
    db_type: Annotated[str, Header(title="Database type", description="Select database you want to retrieve users "
                                                                      "info from: ['redis', 'mdb', 'psql', 'sqlite']",
                                   examples=['redis', 'mdb', 'psql', 'sqlite'])],
    table_name: Annotated[str, Path(title="Table name", description="Name of table you want to perform operation on",
                                    example="title_basics")],

) -> querry_db.GetTableResponses:

    try:
        # send request to the proc_api
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=fun.compose_url(PROC_IP, PROC_PORT) + f"/proc/data",
                headers=httpx.Headers({
                    "db-type": db_type
                }),
                params=httpx.QueryParams({
                    "filters": "True",
                    "table_name": table_name
                })
            )

        # handle responses
        if response.status_code == 200:
            return querry_db.GetTableResponses(
                db_type=db_type,
                table_name=table_name,
                data=response.json()["data"]
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["detail"]
            )

    # handel Validation error
    except exceptions.ResponseValidationError:
        return response.json()

    except httpx.ConnectError:
        raise HTTPException(
            status_code=500,
            detail="Cannot connect to the proc_api"
        )


@data_router.get("/{table_name}/{record_id}", status_code=200,
                 description="Get specified record data from the table", response_description="Database record response")
async def get_record_data(
    db_type: Annotated[str, Header(title="Database type", description="Select database you want to retrieve users "
                                                                      "info from: ['redis', 'mdb', 'psql', 'sqlite']",
                                   examples=['redis', 'mdb', 'psql', 'sqlite'])],
    table_name: Annotated[str, Path(title="Table name", description="Name of table you want to perform operation on",
                                    example="title_basics")],
    record_id: Annotated[str, Path(title="Record identifier", description="Identifies specific record in table",
                                   example="tt0000004")]

) -> querry_db.GetRecordResponses:

    try:
        # send request to the proc_api
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=fun.compose_url(PROC_IP, PROC_PORT) + "/proc/data",
                headers=httpx.Headers({
                    "db-type": db_type
                }),
                params=httpx.QueryParams({
                    "filters": "True",
                    "table_name": table_name,
                    "record_id": record_id
                })
            )

        # handle responses
        if response.status_code == 200:
            return querry_db.GetRecordResponses(
                db_type=db_type,
                table_name=table_name,
                record_id=record_id,
                data=response.json()["data"]
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["detail"]
            )

    # handel Validation error
    except exceptions.ResponseValidationError:
        return response.json()

    except httpx.ConnectError:
        raise HTTPException(
            status_code=500,
            detail="Cannot connect to the proc_api"
        )


@data_router.patch("/{table_name}/{record_id}", status_code=200,
                 description="Update specified record data in the table", response_description="Update confirmation")
async def update_record_data(
    db_type: Annotated[str, Header(title="Database type", description="Select database you want to retrieve users "
                                                                      "info from: ['redis', 'mdb', 'psql', 'sqlite']",
                                   examples=['redis', 'mdb', 'psql', 'sqlite'])],
    table_name: Annotated[str, Path(title="Table name", description="Name of table you want to perform operation on",
                                    example="title_basics")],
    record_id: Annotated[str, Path(title="Record identifier", description="Identifies specific record in table",
                                   example="tt0000004")],
    data: Annotated[dict,
                    Body(title="Data to be updated", description="Body of the data to be updated in the database")]
) -> querry_db.PatchRecordResponses:

    try:
        # send request to the proc_api
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                url=fun.compose_url(PROC_IP, PROC_PORT) + "/proc/data",
                headers=httpx.Headers({
                    "db-type": db_type
                }),
                params=httpx.QueryParams({
                    "table_name": table_name,
                    "record_id": record_id
                }),
                json={"data": data, "table_name": table_name}
            )

        # handle responses
        if response.status_code == 200:
            return querry_db.PatchRecordResponses(
                db_type=db_type,
                table_name=table_name,
                old_data=response.json()["old_data"],
                new_data=response.json()["new_data"]
            )
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["detail"]
            )

    # handel Validation error
    except exceptions.ResponseValidationError:
        return response.json()

    except httpx.ConnectError:
        raise HTTPException(
            status_code=500,
            detail="Cannot connect to the proc_api"
        )