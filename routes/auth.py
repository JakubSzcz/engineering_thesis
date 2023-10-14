from fastapi import APIRouter

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authorization"],
    responses={
        403: {"test": "test"},  # it does not override this!
        404: {"content": "test"}
    }
)
