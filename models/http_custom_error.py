# Contains custom HTTP errors

from fastapi import HTTPException

no_header = HTTPException(
            status_code=400,
            detail="No database header provided"
)

no_body_provided = HTTPException(
            status_code=400,
            detail="Required body content not provided."
)

cannot_connect_to_sys = HTTPException(
            status_code=521,
            detail="Cannot connect to the sys_api"
)

no_such_query = HTTPException(
            status_code=404,
            detail="No such query_id. Possible queries ids are: ['query_1', 'query_2', 'query_1']"
)
