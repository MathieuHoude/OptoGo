import csv
import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

def seed_table_from_csv(connection, table_name, csv_file_path):
    try:
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            # Assuming the CSV header matches the table columns
            columns = ', '.join(csv_reader.fieldnames)
            placeholders = ', '.join(['%s' for _ in csv_reader.fieldnames])
            
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            cursor = connection.cursor()

            for row in csv_reader:
                values = [row[column] for column in csv_reader.fieldnames]
                cursor.execute(insert_query, values)

            connection.commit()
            cursor.close()
            print(f"Data successfully seeded into table: {table_name}")

    except Error as e:
        print(f"Error seeding data into table {table_name}: {e}")
        connection.rollback()

def main():
    # Replace these with your actual database connection details
    # MySQL configuration
    mysql_config = {
        'host': 'localhost',
        'user': os.getenv('USERNAME'),
        'password': os.getenv('PASSWORD'),
        'database': os.getenv('DBNAME')
    }

        
    # Replace 'your_table_name' with the actual table name
    table_name = 'patients'

    # Replace 'path/to/your/data.csv' with the path to your CSV file
    csv_file_path = './DB/seeds/patients.csv'

    # Connect to the MySQL server
    try:
        connection = mysql.connector.connect(**mysql_config)

        if connection.is_connected():
            print("Connected to MySQL database")

            # Seed data into the specified table from the CSV file
            seed_table_from_csv(connection, table_name, csv_file_path)

    except Error as e:
        print(f"Error connecting to MySQL: {e}")

    finally:
        if connection.is_connected():
            connection.close()
            print("Connection to MySQL closed")

if __name__ == "__main__":
    main()
