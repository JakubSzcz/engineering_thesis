# imports
import httpx


# compose valid url
def compose_url(ip: str, port: str,):
    if not ip.startswith("http"):
        return str("http://" + ip + ":" + port)
    else:
        return str(ip + ":" + port)
