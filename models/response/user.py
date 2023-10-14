from pydantic import BaseModel
from datetime import datetime

class User_Response(BaseModel):
    client_id: str
    client_secret: str
    timestamp: datetime
