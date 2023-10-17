from fastapi import APIRouter
import httpx
from datetime import datetime

api_router = APIRouter(
    prefix="/api",
    tags=["api"],
)

