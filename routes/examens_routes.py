from flask import render_template, request, redirect, url_for, session, Blueprint
from mysql.connector import Error
import json

from forms.exam_form import ExamForm
from DB.utils import get_db_connection
from utils import update_session

examens_bp = Blueprint('examens', __name__, url_prefix='/examens')

# route pour la page des examens du patient
@examens_bp.route("/")
def examens():
    index = 4.5
    clinique_id = request.args.get('clinique_id')
    patient_id = request.args.get('patient_id')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT COUNT(*) FROM patients_cliniques WHERE patient_ID = {patient_id} AND clinique_ID = {clinique_id}")
    result = cursor.fetchone()
    if result:
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
    else:
        session["error_message"] = {'title': 'Erreur lors du chargement des examens', 'message': 'Le patient sélectionné ne fréquente pas la clinique sélectionnée.'}
        return redirect(url_for("index"))

# route pour la page d'un examen existant
@examens_bp.route("/<int:examen_id>")
def details(examen_id):
    try:
        index = 6
        clinique_id = request.args.get('clinique_id')
        patient_id = request.args.get('patient_id')
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



# route pour la page d'un nouvel examen
@examens_bp.route("/new")
def new():
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
        print(f"MySQL error: {e}")

@examens_bp.route("/prescription")
def prescription():
    try:
        clinique_id = request.args.get('clinique_id')
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

