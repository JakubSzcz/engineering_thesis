# contains OpenAPI responses examples and other resources for the interactive documentation

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

record_duplication = {
    "content": {
        "application/json": {
            "example": {"detail": "There is already record with such id in the database"}
        }
    },
    "description": "Unique constraints have been violated in database."
}

non_data_provided = {
    "content": {
        "application/json": {
            "example": {"detail": "None of the data to be inserted has been provided"}
        }
    },
    "description": "Any required body field with data has been provided."
}

no_such_record = {
    "content": {
        "application/json": {
            "example": {"detail": "No such record in database"}
        }
    },
    "description": "No record with such id has been found."
}

db_reset_200 = {
    "content": {
        "application/json": {
            "example": {"detail": "Restart of this databases has finished with a success: [psql, mdb, sqlite]"}
        }
    },
    "description": "Database was successfully restored to it's original state."
}

db_reset_500 = {
    "content": {
        "application/json": {
            "example": {"detail": "Restart of this database failed: [redis]"}
        }
    },
    "description": "There was unknown error while trying to reset databases."
}

query_executed = {
    "content": {
        "application/json": {
            "example": {"execution_time": 1.242, "query_description": "test", "query_result": {}}
        }
    },
    "description": "Query results and its execution time"
}


exp_description = """
Experience API purpose is to handle all user related request and returns to users.
## Experience API is responsible for:
* **Create users** 
* **Read users** 
* **Delete users**
* **Generates token**
* **Insert data to Database**.
* **Delete data from Database**.
* **Queries data from Database**.
"""

tags_metadata_exp_api = [
    {
        "name": "Administration panel",
        "description": "Admin operation such us direct access to the database resources"
    },
    {
        "name": "Authorization",
        "description": "Manage authorization related operations, like token generation."
    },
    {
        "name": "User",
        "description": "User related operations to all databases like insert, delete and read"
    },
    {
        "name": "Data",
        "description": "Databases related CRUD operation"
    },
    {
        "name": "Queries",
        "description": "Performance research related operations"
    }
]
