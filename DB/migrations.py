import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

def execute_sql_file(connection, file_path):
    try:
        with open(file_path, 'r') as sql_file:
            sql_script = sql_file.read()
            cursor = connection.cursor()
            cursor.execute(sql_script)
            connection.commit()
            cursor.close()
            print(f"Successfully executed SQL file: {file_path}")
    except Error as e:
        print(f"Error executing SQL file {file_path}: {e}")
        connection.rollback()

def run_migration_scripts(connection, script_folder):
    script_files = [f for f in os.listdir(script_folder) if f.endswith(".sql")]
    script_files.sort()  # Sort the files to execute them in order

    for script_file in script_files:
        script_path = os.path.join(script_folder, script_file)
        execute_sql_file(connection, script_path)

def main():
    # Replace 'path/to/migration/scripts' with the actual path to your SQL migration scripts folder
    migration_scripts_folder = './DB/SQL'

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
            print("Connected to MySQL database")

            # Execute all migration scripts in the specified folder
            run_migration_scripts(connection, migration_scripts_folder)

    except Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print("Connection to MySQL closed")

main()