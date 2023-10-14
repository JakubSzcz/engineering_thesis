from fastapi import APIRouter
import httpx
import asyncio

api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)


async def request(client, url):
    response = await client.get(url)
    return response.text


async def task(url):
    async with httpx.AsyncClient() as client:
        response = await request(client, url)
        print(response)


@api_router.get("/test")
async def test(param: str | None = None):
    url = "http://172.16.0.3:8082/proc/test"
    if param:
        url = url + "?test=" + param
    await task(url)
