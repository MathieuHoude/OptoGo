import re
from flask import Flask, make_response, render_template, request, jsonify, redirect, url_for, session
from dotenv import load_dotenv
import os
import json
import mysql.connector
from mysql.connector import Error
import bcrypt

from forms.patient_form import PatientForm
from forms.exam_form import ExamForm

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

def update_session(cursor, key, query):
    cursor.execute(query)
    session[key] = cursor.fetchone()

    # try:
    #     if session[key]["ID"] != value:
    #         cursor.execute(f'SELECT * FROM {key}s WHERE ID = {value}')
    #         session[key] = cursor.fetchone()
    # except(KeyError): 
    #     cursor.execute(f'SELECT * FROM {key}s WHERE ID = {value}')
    #     session[key] = cursor.fetchone()

def parse_exam_json_objects(dict):
    # Initialize a new dictionary to store extracted key-value pairs
    new_dict = {}

    # Iterate over the original dictionary
    for key, value in dict.items():
        # Try to parse the value as JSON
        try:
            json_data = json.loads(value)
            # If successful, iterate over the JSON object and add key-value pairs to the new dictionary
            for json_key, json_value in json_data.items():
                new_key = f'{key}_{json_key}'  # Creating new keys by concatenating the original key with JSON keys
                new_dict[new_key] = json_value
        except (json.JSONDecodeError, TypeError):
            # If parsing fails, simply copy the key-value pair to the new dictionary
            new_dict[key] = value
    
    return new_dict

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

    clinique = None
    if 'clinique' in session:
        clinique = session['clinique']
    return render_template(
        "index.html",
        index=index,
        optometriste=session["user"],
        cliniques=cliniques,
        clinique=clinique
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
    session["clinique"] = cursor.fetchone()
    cursor.execute(f'SELECT p.* FROM cliniques c JOIN patients_cliniques pc ON c.ID = pc.clinique_ID JOIN patients p ON pc.patient_ID = p.ID WHERE c.ID = {clinique_id} ORDER BY p.last_name;')
    patients = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("patientPage.html",
                           index=index,
                           clinique=session["clinique"],
                           optometriste=session["user"],
                           patients=patients)

# route pour la page des cards de choix
@app.route("/cliniques/<int:clinique_id>/patients/<int:patient_id>")
def choice(clinique_id, patient_id):
    index = 3
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    update_session(cursor, "clinique", f"SELECT * FROM cliniques WHERE ID = {clinique_id}")
    update_session(cursor, "patient", f"SELECT * FROM patients WHERE ID = {patient_id}")
    cursor.close()
    conn.close()
    return render_template("choicePage.html",
                           index=index,
                           clinique=session["clinique"],
                           optometriste=session["user"],
                           patient=session["patient"])

@app.route("/cliniques/patients/new")
def new_patient():
    try:
        index=2.5
        clinique_id = request.args.get('clinique_id')
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM cliniques WHERE ID = {clinique_id}')
        session["clinique"] = cursor.fetchone()
        form = PatientForm()
        cursor.close()
        conn.close()
        return render_template(
            "newPatientPage.html",
            index=index,
            clinique=session["clinique"],
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
    session["patient"] = patient
    form = PatientForm(data=patient)
    confirmation_message = session.pop('confirmation_message', None)
    cursor.close()
    conn.close()
    return render_template("patientInformationPage.html",
                           index=index,
                           clinique=session["clinique"],
                           optometriste=session["user"],
                           patient=session["patient"],
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
    session["patient"] = patient
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
                            clinique=session["clinique"],
                            optometriste=session["user"],
                            patient=session["patient"],
                            form=form)
    


# route pour la page de création d'un nouveau patient
@app.route("/clinique/<int:clinique_id>/patients/new", methods=['GET', 'POST'])
def new_patient_entry(clinique_id):
    """
    This function creates a new patient record in the database.

    Args:
        clinique_id (int): The ID of the clinic where the patient will be registered.

    Returns:
        render_template: A rendered template displaying the new patient form.

    """
    index = 2.5
    form = PatientForm()
    # TODO: On doit ajouter la condition pour le form 
    if request.method == 'POST':
        app.logger.info('Requête POST reçue')
        new_patient_data = {
            'first_name': form.first_name.data,
            'last_name': form.last_name.data,
            'birth_date': form.birth_date.data,
            'gender': form.gender.data,
            'email': form.email.data,
            'phone_number': form.phone_number.data,
            'RAMQ_number': form.RAMQ_number.data,
        }

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql_insert_patient_query = "INSERT INTO patients (first_name, last_name, birth_date, gender, email, phone_number, RAMQ_number) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        params = tuple(new_patient_data.values())
        cursor.execute(sql_insert_patient_query, params)
        conn.commit()

        app.logger.info('Nouveau patient inséré en base de données')

        new_patient_id = cursor.lastrowid

        sql_insert_patient_clinique_query = "INSERT INTO patients_cliniques (patient_ID, clinique_ID) VALUES (%s, %s)"
        cursor.execute(sql_insert_patient_clinique_query, (new_patient_id, clinique_id))
        conn.commit()

        cursor.close()
        conn.close()
        session['confirmation_message'] = {"title": "Ajout complété", "text": f"Les informations de {new_patient_data['first_name']} {new_patient_data['last_name']} ont été ajoutées avec succès."}

    return render_template("newPatientPage.html",  
            index=index,
            clinique=session["clinique"],
            optometriste=session["user"],
            form=form)



# route pour la page d'un examen existant
@app.route("/cliniques/<int:clinique_id>/patients/<int:patient_id>/examens/<int:examen_id>")
def exam_details(clinique_id, patient_id, examen_id):
    try:
        index = 6
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        update_session(cursor, "clinique", f"SELECT * FROM cliniques WHERE ID = {clinique_id}")
        update_session(cursor, "patient", f"SELECT * FROM patients WHERE ID = {patient_id}")
        update_session(cursor, "examen", f"SELECT * FROM examens e LEFT JOIN histoireDeCas h ON e.ID = h.examen_ID WHERE e.ID = {examen_id}" )
        conn.close()
        session["examen"] = parse_exam_json_objects(session["examen"])
        form = ExamForm(data=session["examen"])
        return render_template("examDetailsPage.html",
                            index=index,
                            clinique=session["clinique"],
                            optometriste=session["user"],
                            patient=session["patient"],
                            examen=session["examen"],
                            form=form
                            )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")


@app.route("/cliniques/<int:clinique_id>/prescription")
def prescription(clinique_id):
    try:
        index = 7
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(f'SELECT * FROM addresses WHERE ID = {clinique_id}') 
        addresse_clinique = cursor.fetchone()
   # TODO: Ici jai du hardcode des IDs pour tester la page prescription. A finir
        update_session(cursor, "clinique", f"SELECT * FROM cliniques WHERE ID = {clinique_id}")
        update_session(cursor, "patient", f"SELECT * FROM patients WHERE ID = {104}")
        update_session(cursor, "examen", f"SELECT * FROM examens e LEFT JOIN histoireDeCas h ON e.ID = h.examen_ID WHERE e.ID = {740}" )

        cursor.close()
        conn.close()
        session["examen"] = parse_exam_json_objects(session["examen"])
        form = ExamForm(data=session["examen"])
        return render_template("prescription/prescriptionPage.html",
                            index=index,
                            clinique=session["clinique"],
                            optometriste=session["user"],
                            patient=session["patient"],
                            addresse = addresse_clinique,
                            form=form
                            )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")


# route pour la page des examens du patient
@app.route("/cliniques/<clinique_id>/patients/<patient_id>/examens")
def examens(clinique_id, patient_id):
    index = 4.5
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    update_session(cursor, "clinique", f"SELECT * FROM cliniques WHERE ID = {clinique_id}")
    update_session(cursor, "patient", f"SELECT * FROM patients WHERE ID = {patient_id}")
    cursor.execute(f"SELECT e.ID, e.created_at, o.last_name AS optometriste_last_name, o.first_name AS optometriste_first_name FROM examens e JOIN optometristes o ON e.optometriste_ID = o.ID WHERE e.patient_ID = {patient_id} ORDER BY e.ID;")
    examens = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("examensPage.html",
                           index=index,
                           clinique=session["clinique"],
                           optometriste=session["user"],
                           patient=session["patient"],
                           examens=examens)

# route pour la page d'un nouvel examen
@app.route("/examens/new")
def new_patient_exam():
    try:
        form = ExamForm()
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
                            patient=PatientSelect,
                            form=form
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
    session['clinique'] = cursor.fetchone()
    conn.close()
    response_data = {"message": "Option sélectionnée : " + selected_option, "clinique": session['clinique']}
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
