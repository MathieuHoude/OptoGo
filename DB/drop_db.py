import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

def main():
    # Connect to the MySQL server
    try:
        # MySQL configuration
        mysql_config = {
            'host': os.getenv('HOST'),
            'user': os.getenv('USERNAME'),
            'password': os.getenv('PASSWORD'),
            'database': os.getenv('DBNAME')
        }

        connection = mysql.connector.connect(**mysql_config)

        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("DROP DATABASE optogo;")
            connection.commit()
            cursor.close()
            print(f"Successfully dropped optogo database")
            connection.close()
            print("Connection to MySQL closed")

    except Error as e:
        print(f"Error connecting to MySQL: {e}")

main()