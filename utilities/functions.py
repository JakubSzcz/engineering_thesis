# imports
import httpx
from passlib.context import CryptContext


# compose valid url
def compose_url(ip: str, port: str,):
    if not ip.startswith("http"):
        return str("http://" + ip + ":" + port)
    else:
        return str(ip + ":" + port)


class HashContext:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"])

    def create(self, pwd_plain: str) -> str:
        return self.context.hash(pwd_plain)

    def verify(self, pwd_plain, pwd_hashed) -> bool:
        return self.context.verify(pwd_plain, pwd_hashed)
