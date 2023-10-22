# imports
from datetime import datetime, timezone
import uvicorn
import httpx
from fastapi import FastAPI, Body
from typing import Annotated

from routes.proc import proc_router
from models.auth import *
import utilities.functions as fun
import config as conf

app = FastAPI()

app.include_router(proc_router)


@app.get("/")
def nic():
    return "help"


@app.get("/test")
async def test():
    async with httpx.AsyncClient() as client:
        response = await client.get(fun.compose_url(conf.SYS_IP, conf.SYS_PORT) + "/test")
    return response.json()


# request: Annotated[UserAuthenticateReq, Body()]
@app.post("/auth/user", status_code=200, response_model=Token)
def authenticate_user():
    return Token(access_token="abcdefgh12345678", token_type="Bearer token", expiatory_time=datetime.now())



# launch server
if __name__ == "__main__":
    print("start")
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
