# imports
import uvicorn
from fastapi import FastAPI

from routes.admin import admin_router
from routes.auth import auth_router
from routes.api import api_router
from routes.user import user_router
from cache import Cache


cache = Cache()
app = FastAPI()


app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(api_router)
app.include_router(user_router)


# launch server
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)


