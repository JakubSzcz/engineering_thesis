# libraries imports
import uvicorn
from fastapi import FastAPI

# packages imports
from routes import postgres
from routes import mongodb
from routes import redis

# ### variables ###
app = FastAPI()
app.include_router(postgres.psql_router)
app.include_router(mongodb.mdb_router)
app.include_router(redis.redis_router)


# launch server
if __name__ == "__main__":

    print("[INFO] System API has successfully started.")
    uvicorn.run("main:app", host="127.0.0.1", port=8082, reload=True)
