import sqlite3
from flask import g, current_app

class Database:
    def __init__(self, database_path=None):
        if database_path is None:
            database_path = current_app.config['DATABASE']
        self.database_path = database_path

    def connect(self):
        """Connects to the specific database."""
        conn = sqlite3.connect(self.database_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_db(self):
        """Opens a new database connection if there is none yet for the current application context."""
        if not hasattr(g, 'sqlite_db'):
            g.sqlite_db = self.connect()
        return g.sqlite_db

    def close_db(self, error=None):
        """Closes the database again at the end of the request."""
        if hasattr(g, 'sqlite_db'):
            g.sqlite_db.close()

    def execute_query(self, query, params=()):
        """Execute an insert or update query"""
        db = self.get_db()
        cursor = db.cursor()
        try:
            cursor.execute(query, params)
            db.commit()
            return cursor.lastrowid
        except sqlite3.Error as er:
            print(f"DB query execution failure: {er}")
            db.rollback()
            raise
        finally:
            cursor.close()

    def fetch_query(self, query, params=()):
        """Execute a select query and return the result"""
        db = self.get_db()
        cursor = db.cursor()
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            for row in result:
                print(f"data-> {row}")
            return [dict(row) for row in result]
        except sqlite3.Error as er:
            print(f"DB query execution failure: {er}")
            return None
        finally:
            cursor.close()

    def insert_user(self, user_name, email, hashed_password):
        """Insert a new user into the user table"""
        query = "INSERT INTO user (user_name, email, hashed_password) VALUES (?, ?, ?)"
        params = (user_name, email, hashed_password)
        return self.execute_query(query, params)

    def get_user_by_username(self, user_name):
        """Fetch a user by user_name"""
        query = "SELECT * FROM user WHERE user_name = ?"
        params = (user_name,)
        return self.fetch_query(query, params)
