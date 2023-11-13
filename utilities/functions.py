# imports
from passlib.context import CryptContext
import httpx
from config import *
from fastapi import HTTPException


# compose valid url
def compose_url(ip: str, port: str,):
    if not ip.startswith("http"):
        return str("http://" + ip + ":" + port)
    else:
        return str(ip + ":" + port)


# Hashing class
class HashContext:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"])

    def create(self, pwd_plain: str) -> str:
        return self.context.hash(pwd_plain)

    def verify(self, pwd_plain, pwd_hashed) -> bool:
        return self.context.verify(pwd_plain, pwd_hashed)


# send parallel request to the sys_api in order to restart_db
async def send_async_request_restart_db(db_name):
    async with httpx.AsyncClient() as client:
        response = await client.get(url=compose_url(SYS_IP, SYS_PORT) + "/" + db_name + "/restart")
    return response


# validate database type provided
def validate_db_type(db_type: str):
    if db_type not in db_types:
        raise HTTPException(
            status_code=400,
            detail="Wrong db_type, possible database types: ['redis', 'mdb', 'psql', 'sqlite']"
        )


# validate table name
def validate_table_name(table_name: str):
    if table_name not in tables_names:
        raise HTTPException(
            status_code=422,
            detail="Invalid table name. Possible names: [title_basics, title_episodes, name_basics]"
        )
