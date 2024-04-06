from flask import render_template, request, redirect, url_for, session, Blueprint
from mysql.connector import Error

from forms.patient_form import PatientForm
from DB.utils import get_db_connection

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

# route pour la page des informations du patient
@patients_bp.route("/<int:patient_id>")
def details(patient_id):
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
@patients_bp.route("/<int:patient_id>/edit", methods=['GET', 'POST'])
def edit(patient_id):

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
            return redirect(url_for("patients.details", patient_id=patient['ID']))
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
@patients_bp.route("/new", methods=['GET', 'POST'])
def new():
    """
    This function creates a new patient record in the database.

    Args:
        clinique_id (int): The ID of the clinic where the patient will be registered.

    Returns:
        render_template: A rendered template displaying the new patient form.

    """
    index=2.5
    clinique_id = request.args.get('clinique_id')
    form = PatientForm()
    if request.method == 'POST' and form.validate_on_submit():
        try :
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

            new_patient_id = cursor.lastrowid

            sql_insert_patient_clinique_query = "INSERT INTO patients_cliniques (patient_ID, clinique_ID) VALUES (%s, %s)"
            cursor.execute(sql_insert_patient_clinique_query, (new_patient_id, clinique_id))
            conn.commit()

            cursor.close()
            conn.close()
            session['confirmation_message'] = {"title": "Nouveau patient enregistré", "text": f"Le nouveau patient {new_patient_data['first_name']} {new_patient_data['last_name']} a été ajouté avec succès."}
            return redirect(url_for("patients.details", patient_id=new_patient_id))
        except Error as e:
            return render_template(
                "newPatientPage.html",
                index=index,
                clinique=session["clinique"],
                optometriste=session["user"],
                error_message={'title': 'Erreur lors de la création du nouveau patient', 'message': e.msg, 'code': e.errno},
                form=form)

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(f'SELECT * FROM cliniques WHERE ID = {clinique_id}')
        session["clinique"] = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template(
            "newPatientPage.html",
            index=index,
            clinique=session["clinique"],
            optometriste=session["user"],
            form=form)
    except Error as e:
        print(f"Error with MySQL: {e}")