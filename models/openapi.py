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

cannot_connect_to_sys_api = {
    "content": {
        "application/json": {
            "example": {"detail": "Cannot connect to the sys_api"}
        }
    },
    "description": "There was an internal error in connecting to the sys_api"
}

no_header = {
    "content": {
        "application/json": {
            "example": {"detail": "No database header provided"}
        }
    },
    "description": "There was no header provided"
}

restart_fail = {
    "content": {
        "application/json": {
            "example": {"detail": "Restart of this database failed: redis"}
        }
    },
    "description": "There was unexpected error while restarting database"
}

restart_success = {
    "content": {
        "application/json": {
            "example": {"message": "Restart of this databases has finished with a success: psql"}
        }
    },
    "description": "Chosen database has been successfully restarted"
}

no_body_provided = {
    "content": {
        "application/json": {
            "example": {"detail": "Required body content not provided."}
        }
    },
    "description": "Non body of any table has been provided"
}

data_insert_success = {
    "content": {
        "application/json": {
            "example": {"correlation_id": "123", "status": "inserted","db_source": "psql", "message":
                "Record successfully inserted."}
        }
    },
    "description": "Resource successfully inserted"
}

data_delete_success = {
    "content": {
        "application/json": {
            "example": {"message": "Record deleted"}
        }
    },
    "description": "Resource successfully deleted"
}

data_get_success = {
    "content": {
        "application/json": {
            "example": {"data": {}}
        }
    },
    "description": "Resource successfully retrieved"
}

data_patch_success = {
    "content": {
        "application/json": {
            "example": {"old_data": {}, "new_data": {}}
        }
    },
    "description": "Resource successfully updated"
}

no_such_query = {
    "content": {
        "application/json": {
            "example": {"detail": "No such query_id. Possible queries ids are: ['query_1', 'query_2', 'query_1']"}
        }
    },
    "description": "No valid query id has been provided"
}

