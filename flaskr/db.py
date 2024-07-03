#DB connectivity implementation for the web application
'''import mysql.connector
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
    def execute_query(self, query, params):
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
        except Exception as er:
            print(f"DB query execution failure: {er}")
            raise Exception(F"{er}")
        finally:
            if cursor:
                cursor.close()

        return True
    
    # function to execute database query with variable args
    def execute_vquery(self, query, *params):
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
        except Exception as er:
            print(f"DB query execution failure: {er}")
            raise Exception(F"{er}")
        finally:
            if cursor:
                cursor.close()

        return True
    
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

    # function to fetch records by query and varibale args
    def fetch_vquery(self, query, *params):
        """Execute database query and return the result set as a dictionary
        Arguments:
        query: database query
        params: parameters for the db query
        """
        cursor = None
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, *params)
            result = cursor.fetchall()
            return result
        except Error as er:
            print(f"DB query execution failure: {er}")
            return None
        finally:
            if cursor:
                cursor.close()
    
    # function to call register_user stored procdure
    def call_register_user_test1(self, user_name, email, hashed_password, security_q, security_qa, pub_or_sub):
        #cursor.callproc('register_user', (user_name, email, hashed_password, security_q, security_qa, 1, "@message"))
        """Execute the register_user mysql stored procedure 
        Arguments:
        params: input parameters for the stored procedure
        """
        cursor = None
        try:
            print("----------------------------> test-1")
            cursor = self.connection.cursor()
            cursor.callproc('register_user', (user_name, email, hashed_password, security_q, security_qa, pub_or_sub, "@message"))
            self.connection.commit()

            # Fetch the output message
            cursor.execute("SELECT @message")
            result = cursor.fetchone()
            print(F"result: {result[0]}")
            message = result[0] if result else "Unknown error"
            print(F"returned message: {message}")
        
        except Exception as er:
            print(f"DB query execution failure: {er}")
            raise Exception(F"{er}")
        finally:
            if cursor:
                cursor.close()

        return message

    def call_register_user_test2(self, user_name, email, hashed_password, security_q, security_qa, pub_or_sub):
        """Execute the register_user mysql stored procedure 
        Arguments:
        params: input parameters for the stored procedure
        """
        cursor = None
        message = "Unknown error"
        try:
            print("----------------------------> test-1")
            cursor = self.connection.cursor()

            # Prepare the output parameter
            cursor.execute("SET @out_message = ''")

            # Call the stored procedure
            cursor.callproc('register_user', [user_name, email, hashed_password, security_q, security_qa, pub_or_sub, '@out_message'])

            # Fetch the output message
            cursor.execute("SELECT @out_message")
            result = cursor.fetchone()
            print(result)
            if result is None:
                message = "Unknown Error"
            else:
                print(f"result: {result[0]}")
                message = result[0] if result else "Unknown error"
                print(f"returned message: {message}")

            self.connection.commit()
            
        except Exception as er:
            print(f"DB query execution failure: {er}")
            raise Exception(f"{er}")
        finally:
            if cursor:
                cursor.close()

        return message
    
    def call_register_user(self, user_name, email, hashed_password, security_q, security_qa, pub_or_sub):
        """Execute the register_user mysql stored procedure 
        Arguments:
        params: input parameters for the stored procedure
        """
        cursor = None
        message = "Unknown error"
        try:
            print(F"----------------------------> {user_name}-{email}-{hashed_password}-{security_q}-{security_qa}-{pub_or_sub}")
            cursor = self.connection.cursor()

            # Prepare the output parameter
            cursor.execute("SET @p_message = ''")
            
            # Call the stored procedure and get the OUT value.            
            result_args = cursor.callproc('register_user', [user_name, email, hashed_password, security_q, security_qa, pub_or_sub, "(0, 'CHAR')"])
            #print(F"test----------> : {result_args[6]}")
            if result_args[6]:
                message = result_args[6]
            else:
                message = "Unknown Error"

            # commit the db changes from the connection 
            self.connection.commit()            
        
        except Exception as er:
            print(f"DB query execution failure: {er}")
            raise Exception(f"{er}")
        finally:
            if cursor:
                cursor.close()

        return message

'''


# db.py
# DB connectivity implementation for the web application using SQLite

import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self, config):
        self.config = config
        self.connection = None
    
    # Open a connection to the database
    def connect(self):
        """Initialize the database connection"""
        try:
            print(F"database: {self.config['database']}")
            self.connection = sqlite3.connect(self.config['database'])
            print("Connected to SQLite database")
        except Error as er:
            print(f"Error occurred while connecting to SQLite database: {er}")
    
    # Function to disconnect the established connection with the database
    def disconnect(self):
        """Disconnect the already initialized database connection"""
        if self.connection:
            self.connection.close()
            print("Database connection is disconnected")
    
    # Function to execute database query
    def execute_query(self, query, params):
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
        except Exception as er:
            print(f"DB query execution failure: {er}")
            raise Exception(f"{er}")
        finally:
            if cursor:
                cursor.close()

        return True
    
    # Function to execute database query with variable args
    def execute_vquery(self, query, *params):
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
        except Exception as er:
            print(f"DB query execution failure: {er}")
            raise Exception(f"{er}")
        finally:
            if cursor:
                cursor.close()

        return True
    
    # Function to fetch the records by executing a query
    def fetch_query(self, query, params=None):
        """Execute database query and return the result set as a dictionary
        Arguments:
        query: database query
        params: parameters for the db query
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result
        except Error as er:
            print(f"DB query execution failure: {er}")
            return None
        finally:
            if cursor:
                cursor.close()

    # Function to fetch records by query and variable args
    def fetch_vquery(self, query, *params):
        """Execute database query and return the result set as a dictionary
        Arguments:
        query: database query
        params: parameters for the db query
        """
        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, *params)
            result = cursor.fetchall()
            return result
        except Error as er:
            print(f"DB query execution failure: {er}")
            return None
        finally:
            if cursor:
                cursor.close()

'''
# Sample usage
if __name__ == "__main__":
    db_config = {'database': 'example.db'}
    db = Database(db_config)
    db.connect()

    # Example queries
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_name TEXT NOT NULL,
        email TEXT NOT NULL,
        hashed_password TEXT NOT NULL,
        security_q TEXT NOT NULL,
        security_qa TEXT NOT NULL,
        pub_or_sub INTEGER NOT NULL
    );
    """
    db.execute_query(create_table_query, ())

    insert_query = """
    INSERT INTO users (user_name, email, hashed_password, security_q, security_qa, pub_or_sub)
    VALUES (?, ?, ?, ?, ?, ?);
    """
    db.execute_query(insert_query, ('username', 'email@example.com', 'hashed_password', 'security_question', 'security_answer', 1))

    fetch_query = "SELECT * FROM users;"
    users = db.fetch_query(fetch_query)
    for user in users:
        print(user)

    db.disconnect()
'''