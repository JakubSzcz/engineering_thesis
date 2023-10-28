# libraries imports
import uvicorn
from fastapi import FastAPI

# packages imports
from routes.proc import proc_router
from routes.auth import auth_router
from routes.user import user_router


# ### variables ###
app = FastAPI()

app.include_router(proc_router)
app.include_router(auth_router)
app.include_router(user_router)


# launch server
if __name__ == "__main__":
    print("Process API started successfully.")
    uvicorn.run("main:app", host="127.0.0.1", port=8081, reload=True)
