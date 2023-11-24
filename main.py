# library imports
import uvicorn
from fastapi import FastAPI

# packages imports
from routes.admin import admin_router
from routes.auth import auth_router
from routes.data import data_router
from routes.user import user_router
from routes.queries import query_router
from cache import Cache
from config import *
from models import openapi

# ### variables ###
cache = Cache()
app = FastAPI(
    title="Experience API (EXP_API)",
    description=openapi.exp_description,
    summary="The Experience microservice.",
    version="1.0",
    openapi_tags=openapi.tags_metadata_exp_api
)

# routers includes
app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(data_router)
app.include_router(user_router)
app.include_router(query_router)


# launch server
if __name__ == "__main__":
    print("[INFO] Experience API started successfully.")
    uvicorn.run("main:app", host=EXP_IP, port=int(EXP_PORT), reload=True)
