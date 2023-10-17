from fastapi import APIRouter
from datetime import datetime
from typing import List

from engineering_thesis.models.response import user as user_res_model

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@user_router.get("", status_code=200)
def retrive_users() -> List[user_res_model.User_Response]:
    return {}


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