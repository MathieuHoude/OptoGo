
import os
import mysql.connector
from mysql.connector import Error

def get_db_connection():
    # Replace these with your actual database connection details
    # MySQL configuration
    mysql_config = {
        'host': os.getenv('HOST'),
        'user': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD'),
        'database': os.getenv('DBNAME')
    }

    # Connect to the MySQL server
    try:
        connection = mysql.connector.connect(**mysql_config)

        if connection.is_connected():
            return connection

    except Error as e:
        print(f"Error connecting to MySQL: {e}")