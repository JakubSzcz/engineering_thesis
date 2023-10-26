# imports
from fastapi import APIRouter
import httpx

import config
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
        response = await client.get(fun.compose_url(config.PROC_IP, config.PROC_PORT) + "/test")
    return response.json()


