# imports
from datetime import datetime, timezone
import uvicorn
import httpx
from fastapi import FastAPI

from engineering_thesis.routes.proc import proc_router
import engineering_thesis.utilities.functions as fun
import engineering_thesis.config as conf

app = FastAPI()

app.include_router(proc_router)
client_id="54321"
client_secret="54321"

@app.get("/")
def nic():
    return "help"


@app.get("/test")
async def test():
    async with httpx.AsyncClient() as client:
        response = await client.get(fun.compose_url(conf.SYS_IP, conf.SYS_PORT) + "/test")
    return response.json()



# launch server
if __name__ == "__main__":
    print("start")
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
