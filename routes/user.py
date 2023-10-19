from fastapi import APIRouter
from datetime import datetime
from typing import List
import httpx

from engineering_thesis import config
from engineering_thesis.models.response import user as user_res_model
from engineering_thesis.utilities import functions as fun

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@user_router.get("", status_code=200)
def retrive_users() -> List[user_res_model.User_Response]:
    return {}

@user_router.get("/jwt")
async def test():
    async with httpx.AsyncClient() as client:
        response = await client.get(fun.compose_url(config.PROC_IP, config.PROC_PORT) + "/jwt")
    print(response.json())
    return response.json()



@user_router.get("/{user_id}", status_code=200)
def retrive_user(user_id: int) -> user_res_model.User_Response:
    return {}


@user_router.post("", status_code=201)
def create_user():
    return {}


@user_router.put("/{user_id}", status_code=200)
def edit_user(user_id: int):
    return {}


@user_router.delete("/{user_id}", status_code=200)
def delete_user(user_id: int):
    return {}