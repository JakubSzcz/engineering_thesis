# openapi responses examples
user_deleted = {
    "content": {
        "application/json": {
            "example": {"message": "User deleted"}
        }
    },
    "description": "There is no user with provided username in this database engin"
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

cannot_connect_to_proc_api = {
    "content": {
        "application/json": {
            "example": {"detail": "Cannot connect to the proc_api"}
        }
    },
    "description": "There was an internal error in connecting to the proc_api"
}

incorrect_credentials = {
    "content": {
        "application/json": {
            "example": {"detail": "Incorrect credentials or client does not exists"}
        }
    },
    "description": "Provided credentials was incorrect or does not exists in the selected database"
}
