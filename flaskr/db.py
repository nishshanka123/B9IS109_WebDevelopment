#DB connectivity implementation for the web application
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    # Open a connection to the database
    def connect(self):
        """Initialize the database connection"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as er:
            print(f"Error occurred while connecting to MySQL database : {er}")
    
    # function to disconnect the established connection with the database
    def disconnect(self):
        """Disconnect the already initilized database connection"""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection is disconnected")
    
    # function to execute database query
    def execute_query(self, query, params=None):
        """Execute the database query 
        Arguments:
        query: database query to execute
        params: parameters for the db query
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
        except Error as er:
            print(f"DB query execution failure: {er}")
        finally:
            if cursor:
                cursor.close()
    
    # function to fetch the records by executing a query.
    def fetch_query(self, query, params=None):
        """Execute database query and return the result set as a dictionary
        Arguments:
        query: database query
        params: parameters for the db query
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as er:
            print(f"DB query execution failure: {er}")
            return None
        finally:
            if cursor:
                cursor.close()

