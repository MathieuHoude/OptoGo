import re
from flask import Flask, make_response, render_template, request, jsonify, redirect, url_for, session
from dotenv import load_dotenv
import os
import json
import mysql.connector
from mysql.connector import Error

from DB.utils import get_db_connection

from forms.patient_form import PatientForm
from forms.exam_form import ExamForm
from forms.optometrist_form import OptometristForm

from routes.authentification_routes import auth_bp
from routes.patients_routes import patients_bp
from routes.examens_routes import examens_bp
from routes.clinique_routes import cliniques_bp

app = Flask(__name__)
app.secret_key = 'optogo' #TODO CHANGER!!
# Load environment variables from .env file
load_dotenv()

app.register_blueprint(auth_bp)
app.register_blueprint(patients_bp)
app.register_blueprint(examens_bp)
app.register_blueprint(cliniques_bp)

# Define a list of routes that should not require authentication
ROUTES_NOT_REQUIRING_AUTH = ['auth.login']

# Middleware to check if user is logged in before serving any route
@app.before_request
# This middleware function is used to check if the user is logged in before serving any route.
# If the user is not logged in and the requested route requires authentication,
# it redirects the user to the login page.
def require_login():
    """
    This middleware function is used to check if the user is logged in before serving any route.
    If the user is not logged in and the requested route requires authentication,
    it redirects the user to the login page.
   
    """
    if request.endpoint and request.endpoint not in ROUTES_NOT_REQUIRING_AUTH and not 'user' in session:
        if not request.path.startswith(app.static_url_path):
            return redirect(url_for('auth.login'))

@app.after_request
def after_request(response):
    # Clear the session data when the request is not from the specific blueprint
    if request.blueprint not in ['examens', None] :
        session.pop('histoireDeCas_ID', None)
        session.pop('histoireDeCas', None)
        session.pop('examen', None)
    return response

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index(index=1):
    """
    This function is the main entry point for the application. It handles GET and POST requests to the '/' and '/index' routes.

    Args:
        index (int, optional): An integer representing the current index. Defaults to 1.

    Returns:
        str: A rendered template displaying the main page of the application.

    Raises:
        Exception: If there is an error connecting to the MySQL database.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    form = OptometristForm()
    confirmation_message = None

    cursor.execute('SELECT nombre_patients_du();')
    appointmentsToDo = cursor.fetchone()
    nombre_patients = appointmentsToDo['nombre_patients_du()']


    if request.method == 'POST' and form.validate_on_submit():
        modified_fields = {}
        for field in form:
            if field.name != 'csrf_token' and field.data != session["user"][field.name]:
                modified_fields[field.name] = field.data

        if modified_fields:
            sql_update_query = "UPDATE optometristes SET "
            sql_update_query += ", ".join([f"{field} = %s" for field in modified_fields.keys()])
            sql_update_query += " WHERE id = %s"
            
            # Create a tuple of parameter values in the same order as placeholders
            params = tuple(modified_fields.values()) + (session["user"]["ID"],)

            cursor.execute(sql_update_query, params)
            conn.commit()
        confirmation_message = {"title": "Modifications complétées", "text": f"Vos informations ont été mises à jour avec succès."}
    if request.method == 'GET':
        cursor.execute(f'SELECT o.*, a.street_number, a.street_name, a.city, a.province, a.postal_code FROM optometristes o JOIN addresses a ON o.address_id = a.ID  WHERE o.ID = {session["user"]["ID"]};')
        session["user"] = cursor.fetchone()
        form.process(data=session["user"])
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
        clinique_choisie=clinique,
        form=form,
        confirmation_message=confirmation_message,
        nombre_patients=nombre_patients
    )


# gestion de la requete HTTP pour mettre a jour la clinique
@app.route("/update_clinic", methods=["GET"])
def update_clinic():
    """
    This function is used to update the selected clinic for the logged-in optometrist.
    It retrieves the ID of the selected clinic from the database based on the provided name,
    and stores it in the session for future reference.

    Args:
        selected_option (str): The name of the clinic to be selected.

    Returns:
        json: A JSON response containing a message indicating the selected clinic and its ID.

    Raises:
        Exception: If there is an error connecting to the MySQL database.
    """
    selected_option = request.args.get("selected_option")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f'SELECT ID FROM cliniques WHERE name = "{selected_option}";')
    session['clinique'] = cursor.fetchone()
    conn.close()
    response_data = {"message": f"Option sélectionnée : {selected_option}", "clinique": session['clinique']}
    return jsonify(response_data)

@app.route("/examen-to-do")
def exam_to_do():
    """
    This function is used to display a list of patients who have exams to do.

    Returns:
        str: A rendered template displaying the list of patients with exams to do.

    Raises:
        Exception: If there is an error connecting to the MySQL database.
    """
    try:
        index = 0
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("CALL liste_patients_du()", multi=True)
        patients = cursor.fetchall()
        app.logger.debug(patients)
        return render_template("examsToDoPage.html",
                                patients=patients,
                                optometriste=session["user"],
                                index=index
                                )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")

@app.route("/examen-to-do/<int:patient_id>")
def exam_to_do_patient(patient_id):
    """
    This function is used to display boxes of choice in order to decide what to do concerning this patient.

    Args:
        patient_id (int): The ID of the patient whose exams need to be displayed.

    Returns:
        str: A rendered template displaying the list of patients with exams to do.

    Raises:
        Exception: If there is an error connecting to the MySQL database.
    """
    try:
        index = 3
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM cliniques WHERE ID = (SELECT PC.clinique_ID FROM patients_cliniques PC, patients P WHERE PC.patient_ID = P.ID AND P.ID = {patient_id})")
        clinique = cursor.fetchone()
        session["clinique"] = clinique
        cursor.execute(f"SELECT * FROM patients WHERE ID = {patient_id}")
        patient = cursor.fetchone()
        session["patient"] = patient
        cursor.close()
        conn.close()
        return render_template("choicePage.html",
                                index=index,
                                clinique=session["clinique"],
                                optometriste=session["user"],
                                patient=session["patient"])
    except Error as e:
        print(f"Error connecting to MySQL: {e}")


if __name__ == '__main__':
    app.run(debug=True)
