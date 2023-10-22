from fastapi import APIRouter
from datetime import datetime
from typing import List
import httpx

import config
from models import user
from utilities import functions as fun

user_router = APIRouter(
    prefix="/user",
    tags=["User"],
)

@user_router.get("", status_code=200)
def retrive_users() -> List[user.UserResponse]:
    return {}


@user_router.get("/{user_id}", status_code=200)
def retrive_user(user_id: int) -> user.UserResponse:
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