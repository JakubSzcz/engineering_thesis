from fastapi import HTTPException

cannot_connect_to_proc = HTTPException(
            status_code=521,
            detail="Cannot connect to the Process API."
)
