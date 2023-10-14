# imports
from fastapi import APIRouter

from routes.user import user_router

admin_router = APIRouter(
    prefix="/admin",
    tags=["Administration panel"],
    responses={
  # it does not override this!
        404: {"details": "test"}
    }
)


admin_router.include_router(user_router)


@admin_router.get("/")
def admin_home():
    return {"status": "this is admin endpoint"}

@admin_router.get("/test")
def test():
    return {"status": "working"}


