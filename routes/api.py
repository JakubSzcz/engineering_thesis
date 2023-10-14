from fastapi import APIRouter
import httpx

api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)

async def send_request_to_target_microservice(target_url):
    print("doszło tu0")
    async with httpx.AsyncClient() as client:
        response = await client.get(target_url)
    print("doszło tu1")
    if response.status_code == 200:
        return response.text
    else:
        return f"Request to target microservice failed with status code {response.status_code}"



@api_router.get("/test")
async def test(param: str | None = None):
    url = "http://172.16.0.3:8082/proc/test"
    if param:
        url = url + "?test=" + param
    print("log0-exp_api")
    response = await send_request_to_target_microservice(url)
    return response
