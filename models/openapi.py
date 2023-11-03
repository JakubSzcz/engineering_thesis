# openapi responses examples
user_deleted = {
    "content": {
        "application/json": {
            "example": {"message": "User deleted"}
        }
    },
    "description": "The user with provided username, has been successfully removed"
}
no_username_found = {
    "content": {
        "application/json": {
            "example": {"detail": "No user with a such username"}
        }
    },
    "description": "There is no user with provided username in this database engin"
}

wrong_db_type_header = {
    "content": {
        "application/json": {
            "example": {"detail": "Wrong db_type, possible database types: REDIS, MDB, PSQL, SQLi"}
        }
    },
    "description": "Provided header with database type is not correct"
}

cannot_connect_to_sys_api = {
    "content": {
        "application/json": {
            "example": {"detail": "Cannot connect to the sys_api"}
        }
    },
    "description": "There was an internal error in connecting to the sys_api"
}
