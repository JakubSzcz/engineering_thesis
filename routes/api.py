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
        response = request(client, url)
        result = await asyncio.gather(response)
        print(result)


@api_router.get("/test")
async def test(param: str | None = None):
    url = "http://0.0.0.0:8082/proc/test"
    if param:
        url = url + "?test=" + param
    await task(url)
