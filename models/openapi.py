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

database_empty = {
    "content": {
        "application/json": {
            "example": {"detail": "User database is empty"}
        }
    },
    "description": "There is no records inside database"
}

cannot_connect_to_db = {
    "content": {
        "application/json": {
            "example": {"detail": "Can not connect to the database"}
        }
    },
    "description": "There was an error while connecting to the database container"
}

new_user_created = {
    "content": {
        "application/json": {
            "example": {"detail": "New user created"}
        }
    },
    "description": "New user has been created in chosen database engin"
}
