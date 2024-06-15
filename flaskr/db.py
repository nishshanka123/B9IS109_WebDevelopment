import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self,config):
        """constructor for the Database class to initialize the database connction
        All database operation will be handled by this class and it needs the database
        configuration from the caller
        """
        self.config = config
        self.connection = None
    
    def connect(self):
        """Initialize the database connection"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as er:
            print(f"Error occurred while connecting to MySQL database : {er}")
    
    def disconnect(self):
        """Disconnect the already initilized database connection"""
        if self.connection.is_connected():
            self.connection.close()
            print("Database connection is closed")
    
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
            print(f"DB query excution failure {er}")
        finally:
            if cursor:
                cursor.close()
    
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
            print(f"DB query execution failure : {er}")
            return None
        finally:
            if cursor:
                cursor.close()
                
