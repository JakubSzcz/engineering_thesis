# libraries imports
import uvicorn
from fastapi import FastAPI

# packages imports
from routes.proc import proc_router
from routes.auth import auth_router
from routes.user import user_router
from config import *


# ### variables ###
app = FastAPI(
    title="Process API (PROC_API)",
    description=proc_description,
    summary="Process layer of the microservice.",
    version="1.0",
    openapi_tags=tags_metadata_proc_api
)

app.include_router(proc_router)
app.include_router(auth_router)
app.include_router(user_router)


# launch server
if __name__ == "__main__":
    print("[INFO] Process API started successfully.")
    uvicorn.run("main:app", host=PROC_IP, port=int(PROC_PORT), reload=True)
