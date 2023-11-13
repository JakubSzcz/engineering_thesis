from fastapi import HTTPException

invalid_sql_syntax = HTTPException(
            status_code=500,
            detail="Invalid SQL syntax while inserting into database."
)

record_duplicated = HTTPException(
            status_code=460,
            detail="Such record already exists in the database and violets unique constraints."
)

cannot_connect_to_db = HTTPException(
            status_code=521,
            detail="Cannot connect to the database."
)

lack_of_data = HTTPException(
            status_code=461,
            detail="None of the data to be inserted has been provided"
        )

no_such_record = HTTPException(
                status_code=404,
                detail="There is no such record in the database"
            )
