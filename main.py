# imports
import uvicorn
import httpx
from fastapi import FastAPI

from postgres_db.PostgreSQL import PostgreSQL
from routes import postgres

db = PostgreSQL()
app = FastAPI()
app.include_router(postgres.psql_router)

@app.get("/test")
async def test():
    db.connect(True)
    db.execute("SELECT * FROM users WHERE users.username = 'test_test_test_test'")
    print(db.get_query_results()[0]["username"])
    #user = db.get_query_results()[0]
    db.commit()
    return {"message": "str(user)"}

# launch server
if __name__ == "__main__":
    print("start")
    uvicorn.run("main:app", host="127.0.0.1", port=8082, reload=True)
