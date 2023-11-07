# imports
from fastapi import HTTPException
from passlib.context import CryptContext
import random
from datetime import datetime


class HashContext:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"])

    def create(self, pwd_plain: str) -> str:
        return self.context.hash(pwd_plain)

    def verify(self, pwd_plain, pwd_hashed) -> bool:
        return self.context.verify(pwd_plain, pwd_hashed)


# compose valid url
def compose_url(ip: str, port: str,):
    if not ip.startswith("http"):
        return str("http://" + ip + ":" + port)
    else:
        return str(ip + ":" + port)


# validate database type provided
def validate_db_type(db_type: str):
    if db_type not in ["REDIS", "MDB", "PSQL", "SQLi"]:
        raise HTTPException(
            status_code=400,
            detail="Wrong db_type, possible database types: REDIS, MDB, PSQL, SQLi"
        )


def create_correlation_id(tb_const: str, te_const: str, nb_const):
    # tb - title_basics
    # te - title_episode
    # nb - name_basics
    # ts - timestamp start
    # tf timestamp finish
    return "tb:{tb_const}te:{te_const}nb:{nb_const}ts:{timestamp}tf:{randint}".format(
        tb_const=tb_const, te_const=te_const, nb_const=nb_const,
        timestamp=str(int(datetime.utcnow().timestamp())), randint=random.randint(1000, 9999))
