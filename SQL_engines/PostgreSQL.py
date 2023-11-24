# contains postgres engines/connection/cursor operations
import psycopg2
from psycopg2.extras import RealDictCursor

import config as config


# postgres class
class PostgreSQL:
    # constructor
    def __init__(self):
        self.conn = None
        self.cur = None

    # open connection with db
    def connect(self, real_dict=False):
        if self.conn is None and self.cur is None:
            if real_dict is False:
                self.conn = psycopg2.connect(
                    host=config.PG_HOST,
                    port=config.PG_PORT,
                    database=config.PG_DB,
                    user=config.PG_USR,
                    password=config.PG_PSW
                )
            else:
                self.conn = psycopg2.connect(
                    host=config.PG_HOST,
                    database=config.PG_DB,
                    user=config.PG_USR,
                    password=config.PG_PSW,
                    port=config.PG_PORT,
                    cursor_factory=RealDictCursor
                )
            self.cur = self.conn.cursor()
        else:
            raise ConnectionAlreadyEstablishedException

    # execute sql cmd
    def execute(self, *args):
        if self.cur is not None:
            self.cur.execute(*args)
        else:
            raise NoConnectionEstablishedException

    # get query results
    def get_query_results(self):
        if self.cur is not None:
            return self.cur.fetchall()
        else:
            raise NoConnectionEstablishedException

    # commit and close connection
    def commit(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        self.conn = None
        self.cur = None


class ConnectionAlreadyEstablishedException(Exception):
    pass


class NoConnectionEstablishedException(Exception):
    pass
