from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

PatientSelect, OptoInfoGLobal, ClinicGlobal = {}, {}, {}

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
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT o.*, a.street_number, a.street_name, a.city, a.province, a.postal_code FROM optometristes o JOIN addresses a ON o.address_id = a.ID  WHERE o.ID = 2;')
    OptoInfoGLobal = cursor.fetchone()
    cursor.execute(f'SELECT DISTINCT c.* FROM optometristes o JOIN optometristes_cliniques oc ON o.ID = oc.optometriste_ID JOIN cliniques c ON oc.clinique_ID = c.ID  WHERE o.ID = "{OptoInfoGLobal["ID"]}";')
    cliniques = cursor.fetchall()
    conn.close()
    return render_template(
        "index.html",
        index=index,
        optometriste=OptoInfoGLobal,
        cliniques=cliniques
    )

# route pour la page du patient
@app.route("/cliniques/<clinique_id>")
def clinique(clinique_id):
    index = 2
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM cliniques WHERE ID = {clinique_id};')
    ClinicGlobal = cursor.fetchone()
    cursor.execute(f'SELECT p.* FROM cliniques c JOIN patients_cliniques pc ON c.ID = pc.clinique_ID JOIN patients p ON pc.patient_ID = p.ID WHERE c.ID = {clinique_id} ORDER BY p.last_name;')
    patients = cursor.fetchall()
    conn.close()
    return render_template("patientPage.html",
                           index=index,
                           clinique=ClinicGlobal,
                           patients=patients)

# route pour la page du patient
@app.route("/patients")
def patients():
    index = 2
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM patients ORDER BY last_name LIMIT 100')
    Patients = cursor.fetchall() 
    conn.close()
    return render_template("patientPage.html",
                           index=index,
                           ClinicGlobal=ClinicGlobal,
                           Patients=Patients)

# route pour la page des cards de choix
@app.route("/cliniques/<int:clinique_id>/patients/<int:patient_id>")
def choice(clinique_id, patient_id):
    index = 3
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM cliniques WHERE ID = {clinique_id}')
    ClinicGlobal = cursor.fetchone()
    cursor.execute(f'SELECT * FROM patients WHERE ID = {patient_id}')
    PatientSelect = cursor.fetchone()
    conn.close()
    return render_template("choicePage.html",
                           index=index,
                           clinique=ClinicGlobal,
                           patient=PatientSelect)

# route pour la page des informations du patient
@app.route("/patients/<int:patient_id>")
def patient_details(patient_id):
    index = 4
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM patients WHERE ID = {patient_id}')
    PatientSelect = cursor.fetchone()
    return render_template("patientInformationPage.html",
                           index=index,
                           clinique=ClinicGlobal,
                           patient=PatientSelect
                           )
# route pour la page d'un nouvel examen
@app.route("/examens/new")
def patient_exam():
    try:
        clinique_id = request.args.get('clinique_id')
        patient_id = request.args.get('patient_id')
        index = 5
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM cliniques WHERE ID = {clinique_id}')
        ClinicGlobal = cursor.fetchone()
        cursor.execute(f'SELECT * FROM patients WHERE ID = {patient_id}')
        PatientSelect = cursor.fetchone()
        conn.close()
        return render_template("newExamPage.html",
                            index=index,
                            clinique=ClinicGlobal,
                            patient=PatientSelect
                            )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")


# gestion de la requete HTTP pour mettre a jour la clinique
@app.route("/update_clinic", methods=["GET"])
def update_clinic():
    selected_option = request.args.get("selected_option")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT ID FROM cliniques WHERE name = "{selected_option}";')
    ClinicGlobal = cursor.fetchone()
    conn.close()
    response_data = {"message": "Option sélectionnée : " + selected_option, "clinique": ClinicGlobal}
    return jsonify(response_data)


# gestion de la requete HTTP pour mettre a jour les infos de l'opto
@app.route("/update_opto", methods=["GET"])
def update_opto():
    new_practice_number = request.args.get("practice_number")
    new_adresse = request.args.get("adresse")
    new_phone_number = request.args.get("phone_number")
    OptoInfoGLobal["PracticeNumber"] = new_practice_number
    OptoInfoGLobal["Adresse"] = new_adresse
    OptoInfoGLobal["Phone"] = new_phone_number
    response_data = {"message": "Informations de l'optométriste mises à jour avec succès"}
    return jsonify(response_data)


# gestion de la requete HTTP pour selectionner le patient depuis la page patientsTable.html
@app.route("/select_patient", methods=["GET"])
def select_patient():
    selected_option = request.args.get("selected_patient")
    PatientSelect["name"] = selected_option
    response_data = {"message": "Option sélectionnée : " + selected_option}
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
