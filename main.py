# libraries imports
import uvicorn
from fastapi import FastAPI

# packages imports
from routes import postgres

# ### variables ###
app = FastAPI()
app.include_router(postgres.psql_router)


# launch server
if __name__ == "__main__":
    print("[INFOR] System API has successfully started.")
    uvicorn.run("main:app", host="127.0.0.1", port=8082, reload=True)
