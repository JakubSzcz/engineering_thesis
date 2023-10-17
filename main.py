# imports
import uvicorn
import httpx
from fastapi import FastAPI
import engineering_thesis.utilities.functions as fun
import config as conf


app = FastAPI()

@app.get("/test")
async def test():
    return {"message": "test is working"}

# launch server
if __name__ == "__main__":
    print("start")
    uvicorn.run("main:app", host="127.0.0.1", port=8082, reload=True)
