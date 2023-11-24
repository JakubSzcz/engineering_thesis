# contains endpoints for testing queries performance
# prefix queries
# authorization required: True
# endpoints list:
#   - /info - returns information about predefined queries
#   - /{query_id} - execute provided query on the selected db engines

# libraries import
from fastapi import APIRouter, Header, HTTPException, Path, Depends
from typing import Annotated
from datetime import datetime
import httpx

# packages import
from config import *
from models import querry_db, http_custom_error, openapi
from utilities import functions as fun
from routes.auth import is_user_authenticated

# ### variables ###
query_router = APIRouter(
    prefix="/queries",
    tags=["Queries"],
    dependencies=[Depends(is_user_authenticated)]
)


# ### endpoints ###
@query_router.get("/info", status_code=200, description="Returns information about predefined query",
                  response_description="List of predefined queries")
async def predefined_query_get_info():
    return querry_db.queries_list_info


@query_router.get("/{query_id}", status_code=200,
                  description="Returns result of predefined query", response_description="Query result",
                  responses={
                      200: openapi.query_executed,
                      521: openapi.cannot_connect_to_proc_api
                  })
async def predefined_query_get(
        db_type: Annotated[str, Header(title="Database type", examples=['redis', 'mdb', 'psql', 'sqlite'],
                                       description="Select database you want to retrieve users "
                                                   "info from: ['redis', 'mdb', 'psql', 'sqlite']")],
        query_id: Annotated[str, Path(title="Query identifier", description="Query id you want to execute",
                                      example="query_1")]
):
    # start time counting
    timestamp = datetime.utcnow()

    try:
        # send request to the proc_api
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url=fun.compose_url(PROC_IP, PROC_PORT) + "/proc/query",
                headers=httpx.Headers({
                    "db-type": db_type
                }),
                params=httpx.QueryParams({
                    "query_id": query_id
                }),
                timeout=100000)

        # handle responses
        if response.status_code == 200:
            return {
                "execution_time": str(datetime.utcnow() - timestamp),
                "query_description": querry_db.queries_list_info[query_id],
                "query_result": response.json()
            }
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=response.json()["detail"]
            )

    except httpx.ConnectError:
        raise http_custom_error.cannot_connect_to_proc
