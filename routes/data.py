# libraries import
from fastapi import APIRouter, Header, HTTPException, Body, exceptions
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
@data_router.post("/insert", description="Inserting data to the desired database engine", status_code=201,
                  response_description="Basic information about the insertion such as database type or insertion time",
                  responses={
                    400: openapi.wrong_db_type_header,
                    422: openapi.non_data_provided,
                    460: openapi.record_duplication,
                    500: openapi.cannot_connect_to_proc_api
                  })
async def insert_data_to_db(
        db_type: Annotated[str, Header(title="Database type", description="Select database you want to retrieve users "
                                                                          "info from: ['REDIS', 'MDB','PSQL', 'SQLi']",
                                       examples=["REDIS", "MDB", "PSQL", "SQLi"])],
        title_basics: Annotated[querry_db.InsertTitleBasic | None, Body()] = None,
        name_basics: Annotated[querry_db.InsertNameBasic | None, Body()] = None,
        title_episode: Annotated[querry_db.InsertTitleEpisode | None, Body()] = None
) -> querry_db.InsertResponses:

    start_time = datetime.utcnow()
    # validate db_type
    fun.validate_db_type(db_type)

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
                url=fun.compose_url(PROC_IP, PROC_PORT) + "/proc/insert",
                headers=httpx.Headers({
                    "db-type": user.DatabaseType[db_type].value,
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
