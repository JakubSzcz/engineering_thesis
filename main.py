# imports
import uvicorn
from fastapi import FastAPI
from routes.proc import proc_router

app = FastAPI()

app.include_router(proc_router)
@app.get("/")
def nic():
    return "help"

# launch server
if __name__ == "__main__":
    print("start")
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
