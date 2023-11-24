# contains OpenAPI responses examples and other resources for the interactive documentation

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
    "description": "New user has been created in chosen database engine"
}

data_inserted = {
    "content": {
        "application/json": {
            "example": {"message":  "Record has been inserted successfully."}
        }
    },
    "description": "New data record has been created in chosen database engine"
}

no_data_provided = {
    "content": {
        "application/json": {
            "example": {"detail":  "None of the data to be inserted has been provided"}
        }
    },
    "description": "No required data has been provided to be inserted in database"
}

no_such_record = {
    "content": {
        "application/json": {
            "example": {"detail":  "There is no such record in the database"}
        }
    },
    "description": "No record with provided id has been found"
}

get_all_data = {
    "content": {
        "application/json": {
            "example": {"message": '{"data": {\n"title_basics": {},\n title_episodes": {},\n"name_basics": {}\n}}'}
        }
    },
    "description": "All data from database"
}

get_data = {
    "content": {
        "application/json": {
            "example": {"message": '{"data": {}'}
        }
    },
    "description": "Data from database"
}
