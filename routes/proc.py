from fastapi import APIRouter

proc_router = APIRouter(
    prefix="/proc",
    tags=["proc"],
)

@proc_router.get("/test")
def test(variable: str | None = None):
    print("log1")
    if variable:
        return {"message": variable}
    else:
        return {"message": "test"}
