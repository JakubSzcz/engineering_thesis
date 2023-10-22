# imports
import uvicorn
import httpx
from fastapi import FastAPI
from postgres_db.PostgreSQL import PostgreSQL

db = PostgreSQL()
app = FastAPI()

@app.get("/test")
async def test():
    db.connect(True)
    db.execute("SELECT * FROM users")
    user = db.get_query_results()[0]
    db.commit()
    return {"message": str(user)}

# launch server
if __name__ == "__main__":
    print("start")
    uvicorn.run("main:app", host="127.0.0.1", port=8082, reload=True)
