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
# def before_request():
#     session.pop('confirmation_message', None)
def require_login():
    if request.endpoint and request.endpoint not in ROUTES_NOT_REQUIRING_AUTH and not 'user' in session:
        if not request.path.startswith(app.static_url_path):
            return redirect(url_for('auth.login'))

@app.route("/", methods=['GET', 'POST'])
@app.route("/index", methods=['GET', 'POST'])
def index():
    index = 1
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    form = OptometristForm()
    confirmation_message = None
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
        confirmation_message=confirmation_message
    )


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

if __name__ == '__main__':
    app.run(debug=True)
