# library imports
from passlib.context import CryptContext
from config import *
from fastapi import HTTPException, Body, Header, Query
from typing import Annotated
from pydantic import ValidationError
import httpx
import re


# packages imports
from models import querry_db


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
def validate_db_type(db_type: Annotated[str, Header(title="Database type", description="Database type destination",
                                                    example="psql")]):
    if db_type not in db_types:
        raise HTTPException(
            status_code=400,
            detail="Wrong db_type, possible database types: ['redis', 'mdb', 'psql', 'sqlite']"
        )
    return db_type


# validate table name
def validate_table_name(table_name: Annotated[str, Query(title="Table name", examples=["title_basics"])]):
    if table_name not in tables_names:
        raise HTTPException(
            status_code=422,
            detail="Invalid table name. Possible names: [title_basics, title_episodes, name_basics]"
        )
    return table_name


# validate table name
def validate_table_name_optional(table_name: str):
    if table_name not in tables_names:
        raise HTTPException(
            status_code=422,
            detail="Invalid table name. Possible names: [title_basics, title_episodes, name_basics]"
        )


# validate structure of the data provided
async def validate_db_structure(data: Annotated[dict, Body(title="Data to be updated",
                                                        description="Body of the data to be updated in the database")]):
    valid_field = False

    if data["table_name"] == "title_basics":
        # check if any valid field was provided
        for key in data["data"]:
            if key in models_fields["title_basics"]:
                valid_field = True
                break
        if valid_field:
            try:
                querry_db.UpdateTitleBasic(**data["data"])
            except ValidationError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid data provided"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="No valid field was provided"
            )

    elif data["table_name"] == "name_basics":

        # check if any valid field was provided
        for key in data["data"]:
            if key in models_fields["name_basics"]:
                valid_field = True
                break
        if valid_field:
            try:
                querry_db.UpdateNameBasic(**data["data"])
            except ValidationError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid data provided"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="No valid field was provided"
            )

    elif data["table_name"] == "title_episodes":

        # check if any valid field was provided
        for key in data["data"]:
            if key in models_fields["title_episodes"]:
                valid_field = True
                break
        if valid_field:
            try:
                querry_db.UpdateTitleEpisode(**data["data"])
            except ValidationError:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid data provided"
                )
        else:
            raise HTTPException(
                status_code=400,
                detail="No valid field was provided"
            )
    return data


# validate record_id
def validate_record_id(record_id: Annotated[str, Query(title="Record identifier", examples=["tt0000004"])]):
    # pre validate record_id
    if not re.match(r"^[tnm][tnm]\d+$", str(record_id)):
        raise HTTPException(
            status_code=400,
            detail="Invalid record_id format. Record id should looks like {t/n/m}{t/n/m}XXXXX, X- digit"
        )
    return record_id


# validate record_id
def validate_record_id_optional(record_id: str):
    # pre validate record_id
    if not re.match(r"^[tnm][tnm]\d+$", str(record_id)):
        raise HTTPException(
            status_code=400,
            detail="Invalid record_id format. Record id should looks like {t/n/m}{t/n/m}XXXXX, X- digit"
        )
