# libraries imports
import uvicorn
from fastapi import FastAPI

# packages imports
from config import *
from routes import postgres
from routes import mongodb
from routes import redis
from routes import sqlite

# ### variables ###
app = FastAPI(
    title="System API (SYS_API)",
    description=sys_description,
    summary="System layer of the microservice.",
    version="1.0",
    openapi_tags=tags_metadata_sys_api
)

# api routers includes
app.include_router(postgres.psql_router)
app.include_router(mongodb.mdb_router)
app.include_router(redis.redis_router)
app.include_router(sqlite.sqli_router)


# launch server
if __name__ == "__main__":
    print("[INFO] System API has successfully started.")
    uvicorn.run("main:app", host="127.0.0.1", port=8082, reload=True)
