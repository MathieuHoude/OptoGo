import re
from flask import Flask, make_response, render_template, request, jsonify, redirect, url_for, session
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
import bcrypt

from forms.patient_form import PatientForm

app = Flask(__name__)
app.secret_key = 'optogo' #TODO CHANGER!!
# Load environment variables from .env file
load_dotenv()

# Define a list of routes that should not require authentication
ROUTES_NOT_REQUIRING_AUTH = ['login']

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

# Middleware to check if user is logged in before serving any route
@app.before_request
# def before_request():
#     session.pop('confirmation_message', None)
def require_login():
    if request.endpoint and request.endpoint not in ROUTES_NOT_REQUIRING_AUTH and not 'user' in session:
        if not request.path.startswith(app.static_url_path):
            return redirect(url_for('login'))

@app.route("/")
@app.route("/index")
def index():
    index = 1
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT o.*, a.street_number, a.street_name, a.city, a.province, a.postal_code FROM optometristes o JOIN addresses a ON o.address_id = a.ID  WHERE o.ID = {session["user"]["ID"]};')
    session["user"] = cursor.fetchone()
    cursor.execute(f'SELECT DISTINCT c.* FROM optometristes o JOIN optometristes_cliniques oc ON o.ID = oc.optometriste_ID JOIN cliniques c ON oc.clinique_ID = c.ID  WHERE o.ID = "{session["user"]["ID"]}";')
    cliniques = cursor.fetchall()
    cursor.close()
    conn.close()

    clinique_choisie = None
    if 'clinique_choisie' in session:
        clinique_choisie = session['clinique_choisie']
    return render_template(
        "index.html",
        index=index,
        optometriste=session["user"],
        cliniques=cliniques,
        clinique_choisie=clinique_choisie
    )

# route pour la page d'authentification
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM optometristes WHERE email = "{email}"')
        optometriste = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if(optometriste is None):
            session["login_error"] = {'title': 'Erreur authentification', 'text': 'Veuillez vérifier votre email ou mot de passe'}
            return redirect(url_for("login"))
        
        # Check if the provided password matches the stored hashed password
        if bcrypt.checkpw(password.encode('utf-8'), optometriste['password'].encode()):
            session.pop('login_error', None)
            session["user"] = optometriste
            return redirect(url_for("index"))
        else:
            session["login_error"] = {'title': 'Erreur authentification', 'text': 'Veuillez vérifier votre email ou mot de passe'}
            return redirect(url_for("login"))
    else :
        if 'user' in session:
            return redirect(url_for("index"))
        else:
            return render_template("loginPage.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))

# route pour la page du patient
@app.route("/cliniques/<clinique_id>")
def clinique(clinique_id):
    index = 2
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM cliniques WHERE ID = {clinique_id};')
    session["clinique_choisie"] = cursor.fetchone()
    cursor.execute(f'SELECT p.* FROM cliniques c JOIN patients_cliniques pc ON c.ID = pc.clinique_ID JOIN patients p ON pc.patient_ID = p.ID WHERE c.ID = {clinique_id} ORDER BY p.last_name;')
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("patientPage.html",
                           index=index,
                           clinique=session["clinique_choisie"],
                           optometriste=session["user"],
                           patients=patients)


# route pour la page du patient
@app.route("/patients") #TODO voir si c'est nécessaire
def patients():
    index = 2
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM patients ORDER BY last_name LIMIT 100')
    Patients = cursor.fetchall()
    cursor.close()
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
    session["clinique_choisie"] = cursor.fetchone()
    cursor.execute(f'SELECT * FROM patients WHERE ID = {patient_id}')
    session["patient_choisi"] = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("choicePage.html",
                           index=index,
                           clinique=session["clinique_choisie"],
                           optometriste=session["user"],
                           patient=session["patient_choisi"])

@app.route("/cliniques/patients/new")
def new_patient():
    try:
        index=2.5
        clinique_id = request.args.get('clinique_id')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM cliniques WHERE ID = {clinique_id}')
        session["clinique_choisie"] = cursor.fetchone()
        form = PatientForm()
        cursor.close()
        conn.close()
        return render_template(
            "newPatientPage.html",
            index=index,
            clinique=session["clinique_choisie"],
            optometriste=session["user"],
            form=form)
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return "An error occurred while processing your request.", 500


# route pour la page des informations du patient
@app.route("/patients/<int:patient_id>")
def patient_details(patient_id):
    index = 4
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM patients WHERE ID = {patient_id}')
    patient = cursor.fetchone()
    session["patient_choisi"] = patient
    form = PatientForm(data=patient)
    confirmation_message = session.pop('confirmation_message', None)
    cursor.close()
    conn.close()
    return render_template("patientInformationPage.html",
                           index=index,
                           clinique=session["clinique_choisie"],
                           optometriste=session["user"],
                           patient=session["patient_choisi"],
                           confirmation_message=confirmation_message,
                           form=form)

# route pour la page de modification des informations du patient
@app.route("/patients/<int:patient_id>/edit", methods=['GET', 'POST'])
def patient_edit(patient_id):

    index = 4
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT * FROM patients WHERE ID = {patient_id}')
    patient = cursor.fetchone()
    session["patient_choisi"] = patient
    form = PatientForm(data=patient)

    if request.method == 'POST' and form.validate_on_submit():
        modified_fields = {}
        for field in form:
            if field.name != 'csrf_token' and field.data != patient[field.name]:
                modified_fields[field.name] = field.data

        if modified_fields:
            sql_update_query = "UPDATE patients SET "
            sql_update_query += ", ".join([f"{field} = %s" for field in modified_fields.keys()])
            sql_update_query += " WHERE id = %s"
            
            # Create a tuple of parameter values in the same order as placeholders
            params = tuple(modified_fields.values()) + (patient_id,)

            cursor.execute(sql_update_query, params)
            conn.commit()
            cursor.close()
            conn.close()
            session['confirmation_message'] = {"title": "Modifications complétées", "text": f"Les informations de {patient['first_name']} {patient['last_name']} ont été mises à jour avec succès."}
            return redirect(url_for("patient_details", patient_id=patient['ID']))

    else:
        cursor.close()
        conn.close()
        return render_template("patientEditPage.html",
                            index=index,
                            clinique=session["clinique_choisie"],
                            optometriste=session["user"],
                            patient=session["patient_choisi"],
                            form=form)

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
                            optometriste=session["user"],
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
    session['clinique_choisie'] = cursor.fetchone()
    conn.close()
    response_data = {"message": "Option sélectionnée : " + selected_option, "clinique": session['clinique_choisie']}
    return jsonify(response_data)



"""
This function updates the optometrist's information in the database.

Args:
    request_data (dict): The request data containing the new practice number,
        address, and phone number.

Returns:
    dict: A dictionary containing the message, updated practice number, address,
        and phone number.
"""
@app.route("/update_opto", methods=["POST"])
def update_opto():
    request_data = request.json
    new_practice_number = request_data.get("practice_number")
    new_adresse = request_data.get("adresse")
    new_phone_number = request_data.get("phone_number")
    session['user']["PracticeNumber"] = new_practice_number
    session['user']["Adresse"] = new_adresse
    session['user']["Phone"] = new_phone_number

    response_data = {
        "message": "Informations de l'optométriste mises à jour avec succès",
        "PracticeNumber": new_practice_number,
        "Adresse": new_adresse,
        "Phone": new_phone_number
    }

    response = make_response(jsonify(response_data))
    response.status_code = 200
    return response


"""
    This function is used to verify the RAMQ field in the patient's record.

    Args:
        request_data (dict): The request data containing the RAMQ field.

    Returns:
        dict: A dictionary containing the validation result and message.

    Raises:
        ValueError: If the RAMQ field is empty or contains invalid characters.
"""
@app.route("/verif_ramq", methods=["POST"])
def verif_ramq():
    request_data = request.json
    ramq = request_data.get("ramq").replace(" ", "")
    if ramq is None:
        return jsonify({"valid": False, "message": "Le champ RAMQ est vide."})
    if len(ramq) == 0:
        return jsonify({"valid": False, "message": "Le champ RAMQ est vide."})
    if len(ramq) > 12:
        return jsonify({"valid": False, "message": "Le champ RAMQ est trop long."})
    if not re.match("^[A-Za-z]+$", ramq[:3]):
        return jsonify({"valid": False, "message": "Les 4 premiers caractères du champ RAMQ doivent être des lettres alphabétiques."})
    if not re.match("^\d+$", ramq[3:]):
        return jsonify({"valid": False, "message": "Les caractères restants du champ RAMQ doivent être des chiffres."})
    return jsonify({"valid": True, "message": "Le champ RAMQ est valide."})




if __name__ == '__main__':
    app.run(debug=True)
