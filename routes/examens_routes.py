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
    """
    This function is responsible for rendering the exams page for a specific patient and clinic.

    Parameters:
    - clinique_id (int): The ID of the clinic.
    - patient_id (int): The ID of the patient.

    Returns:
    - A rendered HTML template for the exams page.

    Raises:
    - Error: If there is an issue with the database connection.

    This function first checks if the patient is associated with the selected clinic. If so, it fetches the patient and clinic data from the database and passes it to the template along with the exams data. If not, it sets an error message in the session and redirects to the index page.
    """
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
    """
    This function is responsible for rendering the details page of a specific exam.
   
    Parameters:
    - examen_id (int): The ID of the exam to be displayed.
    - clinique_id (int): The ID of the clinic.
    - patient_id (int): The ID of the patient.

    Returns:
    - A rendered HTML template for the exam details page.

    Raises:
    - Error: If there is an issue with the database connection.

    it fetches the exam data along with the patient and clinic data from the database and passes it to the template.
    """
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
def new(form=None, clinique_id=None, patient_id=None, index=None):
    """
    This function is responsible for rendering the page for creating a new exam.

    Parameters:
    - form (Flask_Form.FlaskForm): A Flask form object for handling form data.
    - clinique_id (int): The ID of the clinic.
    - patient_id (int): The ID of the patient.
    - index (int): An index number for the page.

    Returns:
    - A rendered HTML template for the new exam page.

    Raises:
    - Error: If there is an issue with the database connection.

    This function first fetches the clinic and patient data from the database using the provided IDs. It then passes this data along with the form object to the template for rendering the new exam page.
    """
    try:
        if form is None:
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

@examens_bp.route("/<int:examen_id>/prescription")
def prescription(examen_id):
    """
    This function is responsible for rendering the prescription page of a specific exam.

    Parameters:
    - examen_id (int): The ID of the exam to be displayed.
    - clinique_id (int): The ID of the clinic.
    - patient_id (int): The ID of the patient.

    Returns:
    - A rendered HTML template for the exam prescription page.

    Raises:
    - Error: If there is an issue with the database connection.

    It fetches the exam data along with the patient and clinic data from the database and passes it to the template. The function also fetches the address of the clinic and includes it in the template.
    """
    try:
        clinique_id = request.args.get('clinique_id')
        patient_id = request.args.get('patient_id')
        index = 7
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(f'SELECT * FROM addresses WHERE ID = {clinique_id}') 
        addresse_clinique = cursor.fetchone()

        update_session(cursor, "clinique", f"SELECT * FROM cliniques WHERE ID = {clinique_id}")
        update_session(cursor, "patient", f"SELECT * FROM patients WHERE ID = {patient_id}")
        update_session(cursor, "examen", f"SELECT * FROM examens e LEFT JOIN histoireDeCas h ON e.ID = h.examen_ID WHERE e.ID = {examen_id}" )

        cursor.close()
        conn.close()
        session["examen"] = parse_exam_json_objects(session["examen"])
        form = ExamForm(data=session["examen"])
        return render_template("prescription/prescriptionPage.html",
                            index=index,
                            clinique=session["clinique"],
                            optometriste=session["user"],
                            patient=session["patient"],
                            examen=session["examen"],
                            addresse = addresse_clinique,
                            form=form
                            )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")



def parse_exam_json_objects(dict):
    """
    This function takes a dictionary where some values are JSON strings.
    It parses these JSON strings and adds the parsed key-value pairs to a new dictionary.

    Parameters:
    - dict (dict): The input dictionary where some values are JSON strings.

    Returns:
    - dict: A new dictionary where the parsed JSON strings are added as key-value pairs.

    Raises:
    - json.JSONDecodeError: If a JSON string cannot be parsed.
    - TypeError: If a value in the input dictionary is not a string.

    The function iterates over the input dictionary. For each key-value pair, it tries to parse the value as a JSON string. If successful, it iterates over the JSON object and adds the key-value pairs to the new dictionary. The new keys are created by concatenating the original key with the JSON keys. If parsing fails, the original key-value pair is simply copied to the new dictionary.
    """
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

