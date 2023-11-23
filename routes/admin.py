# library imports
from fastapi import APIRouter, Header, Path
from typing import Annotated
import httpx

# package imports
from config import *
from utilities import functions as fun
from models import openapi


# ### variables ###
admin_router = APIRouter(
    prefix="/admin",
    tags=["Administration panel"]
)


# ### endpoints ###
@admin_router.get("/db_restart", description="Restarts databases instances to its original state.", status_code=200,
                  responses={
                      200: openapi.db_reset_200,
                      400: openapi.wrong_db_type_header,
                      500: openapi.db_reset_500,
                      521: openapi.cannot_connect_to_proc_api
                  })
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


@admin_router.get("/data/prepare", description="Basic preprocessing for data from IMDB database "
                                               "such as removing null values, appropriate for all db engines",
                  status_code=200)
def restart_db_universal():

    print("Data preparation process started.")
    fun.process_and_save_data(title_episodes_path, title_episodes_path_url, "te")
    print("1/3")

    fun.process_and_save_data(title_basics_path, title_basics_path_url,"tb")
    print("2/3")

    fun.process_and_save_data(name_basics_path, name_basics_path_url, "nb")
    print("3/3")
    print("Data preparation process finished.")

    return {"message": "Datasets prepared"}


@admin_router.get("/data/prepare/{db_type}", description="Prepares data from IMDb's database to align with the "
                                                         "specific database.", status_code=200)
def restart_db_specified(
        db_type: Annotated[str, Path()]
):

    print(f"[INFO] Data preparation process for {db_type} started.")
    print("[INFO] 1/3 - title_episodes")
    fun.process_and_save_data(title_episodes_path, title_episodes_path_url, "te", db_type)
    print("[INFO] Finished - title_episodes")

    print("[INFO] 2/3 - title_basics")
    fun.process_and_save_data(title_basics_path, title_basics_path_url, "tb", db_type)
    print("[INFO] Finished - title_basics")

    print("[INFO] 3/3 - name_basics")
    fun.process_and_save_data(name_basics_path, name_basics_path_url, "nb", db_type)
    print("[INFO] Finished - name_basics")
    print("[INFO] Data preparation process finished.")
    # fun.process_and_save_data(test_path, test_path_url, "tb", db_type)

    return {"message": f"Datasets for {db_type} prepared"}
