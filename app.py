from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

ClinicGlobal = {}

def get_db_connection():
    # Replace these with your actual database connection details
    # MySQL configuration
    mysql_config = {
        'host': 'localhost',
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


@app.route("/")
@app.route("/index")
def index():
    index = 1
    return render_template("index.html", index=index)


@app.route("/patients")
def patients():
    index = 2
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM patients LIMIT 100')
    patients = cursor.fetchall() 
    conn.close()
    return render_template("patientPage.html", index=index, ClinicGlobal=ClinicGlobal["clinique"], patients=patients)


@app.route("/update_clinic", methods=["GET"])
def update_clinic():
    selected_option = request.args.get("selected_option")
    ClinicGlobal["clinique"] = selected_option
    response_data = {"message": "Option sélectionnée : " + selected_option}
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)