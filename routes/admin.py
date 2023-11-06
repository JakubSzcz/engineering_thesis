# imports
from fastapi import APIRouter, Header
from typing import Annotated
import httpx
import pandas as pd

from config import *
from utilities import functions as fun


admin_router = APIRouter(
    prefix="/admin",
    tags=["Administration panel"]
)


@admin_router.get("/")
def admin_home():
    return {"status": "this is admin endpoint"}


@admin_router.get("/test")
async def test():
    async with httpx.AsyncClient() as client:
        response = await client.get(fun.compose_url(PROC_IP, PROC_PORT) + "/test")
    return response.json()


@admin_router.get("/db_restart", description="Restarts databases instances.", status_code=200)
async def restart_db(
        redis: Annotated[bool | None, Header(title="Redis Flag", description="Indicates to restart Redis database",
                                             example="True")] = None,
        postgres: Annotated[bool | None, Header(title="Postgres Flag", description="Indicates to restart PostgreSQL"
                                                                                   " database", example="True")] = None,
        mongo: Annotated[bool | None, Header(title="Mongo Flag", description="Indicates to restart MongoDB database",
                                             example="True")] = None,
        sqlite: Annotated[bool | None, Header(title="SQLite Flag", description="Indicates to restart SQLite database",
                                              example="True")] = None
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=fun.compose_url(PROC_IP, PROC_PORT) + "/proc/db_restart",
            headers=httpx.Headers({
                "redis": ("True" if redis is not None else "False"),
                "postgres": ("True" if postgres is not None else "False"),
                "mongo": ("True" if mongo is not None else "False"),
                "sqlite": ("True" if sqlite is not None else "False")
            }),
            timeout=10.0
        )
    return response.json()


@admin_router.get("/data/prepare", description="Prepares data from IMDb's database.", status_code=200)
def restart_db():
    print("Data preparation process started.")
    data = (pd.read_csv(title_episodes_path, sep='\t', na_values=["\\N"]).
            replace("'", "%27", regex=True).fillna(-1))
    data.to_csv(title_episodes_path_url, sep='\t', index=False)
    print("1/3")
    data = (pd.read_csv(title_basics_path, sep='\t', na_values=["\\N"]).
            replace("'", "%27", regex=True).fillna(-1))
    data.to_csv(title_basics_path_url, sep='\t', index=False)
    print("2/3")
    data = (pd.read_csv(name_basics_path, sep='\t', na_values=["\\N"]).
            replace("'", "%27", regex=True).fillna(-1))
    data.to_csv(name_basics_path_url, sep='\t', index=False)
    print("3/3")
    print("Data preparation process finished.")
    return {"message": "Datasets prepared"}

