# imports
import uvicorn
from fastapi import FastAPI

from routes.admin import admin_router
from routes.auth import auth_router
from routes.api import api_router


app = FastAPI()

app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(api_router)


# launch server
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)

