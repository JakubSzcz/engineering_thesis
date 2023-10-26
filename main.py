# imports
from datetime import datetime, timezone
import uvicorn
import httpx
from fastapi import FastAPI, Body
from typing import Annotated

from routes.proc import proc_router
from routes.auth import auth_router
import utilities.functions as fun
import config as conf

app = FastAPI()

app.include_router(proc_router)
app.include_router(auth_router)


# launch server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
