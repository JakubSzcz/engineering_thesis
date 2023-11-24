# contains sqlite engines/connection/cursor operations
import sqlite3


# postgres class
class SQLite:
    # constructor
    def __init__(self):
        self.conn = None
        self.cur = None

    # open connection with db
    def connect(self):
        if self.conn is None and self.cur is None:
            self.conn = sqlite3.connect("./SQL_engines/sqlitedb.db")
            self.conn.row_factory = sqlite3.Row
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
