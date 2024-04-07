from flask import render_template, request, redirect, url_for, session, Blueprint
from mysql.connector import Error

from forms.patient_form import PatientForm
from forms.address_form import AddressForm
from DB.utils import get_db_connection
from utils import update_session

patients_bp = Blueprint('patients', __name__, url_prefix='/patients')

# route pour la page des informations du patient
@patients_bp.route("/<int:patient_id>")
def details(patient_id):
    """
    This function retrieves and displays the details of a specific patient.

    Args:
        patient_id (int): The ID of the patient whose details are to be displayed.

    Returns:
        A rendered template: A HTML page displaying the details of the specified patient.

    """
    index = 4
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    update_session(cursor, "patient", f'SELECT * FROM patients WHERE ID = {patient_id}')
    patient_form = PatientForm(data=session['patient'])
    cursor.execute(f"SELECT * FROM addresses WHERE ID = {session['patient']['address_ID']}")
    address = cursor.fetchone()
    address_form = AddressForm(data=address)
    confirmation_message = session.pop('confirmation_message', None)
    cursor.close()
    conn.close()
    return render_template("patientInformationPage.html",
                           index=index,
                           clinique=session["clinique"],
                           optometriste=session["user"],
                           patient=session["patient"],
                           confirmation_message=confirmation_message,
                           patient_form=patient_form,
                           address_form=address_form)

# route pour la page de modification des informations du patient
@patients_bp.route("/<int:patient_id>/edit", methods=['GET', 'POST'])
def edit(patient_id):
    """
    This function allows the editing of a specific patient's information.

    Args:
        patient_id (int): The ID of the patient whose information is to be edited.

    Returns:
        A rendered template: A HTML page displaying the form for editing the specified patient's information.

    If the request method is POST and the form is valid, the function updates the patient's information in the database and redirects to the details page of the edited patient.

    If the request method is GET, the function retrieves the patient's information from the database, populates the form with the current information, and renders the edit page.

    """
    index = 4
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    update_session(cursor, "patient", f'SELECT * FROM patients WHERE ID = {patient_id}')
    address_form = AddressForm()
    patient_form = PatientForm()
    if request.method == 'POST' and patient_form.validate_on_submit():

        modified_fields = {}
        for field in patient_form:
            if field.name != 'csrf_token' and field.data != session['patient'][field.name]:
                modified_fields[field.name] = field.data

        if modified_fields:
            sql_update_query = "UPDATE patients SET "
            sql_update_query += ", ".join([f"{field} = %s" for field in modified_fields.keys()])
            sql_update_query += " WHERE id = %s"
            
            # Create a tuple of parameter values in the same order as placeholders
            params = tuple(modified_fields.values()) + (patient_id,)

            cursor.execute(sql_update_query, params)
            conn.commit()

        modified_fields = {}
        cursor.execute(f"SELECT * FROM addresses WHERE ID = {session['patient']['address_ID']}")
        address = cursor.fetchone()
        for field in address_form:
            if field.name != 'csrf_token' and field.data != address[field.name]:
                modified_fields[field.name] = field.data

        if modified_fields:
            sql_update_query = "UPDATE addresses SET "
            sql_update_query += ", ".join([f"{field} = %s" for field in modified_fields.keys()])
            sql_update_query += " WHERE id = %s"
            
            # Create a tuple of parameter values in the same order as placeholders
            params = tuple(modified_fields.values()) + (address['ID'],)

            cursor.execute(sql_update_query, params)
            conn.commit()

        cursor.close()
        conn.close()
        session['confirmation_message'] = {"title": "Modifications complétées", "text": f"Les informations de {session['patient']['first_name']} {session['patient']['last_name']} ont été mises à jour avec succès."}
        return redirect(url_for("patients.details", patient_id=session['patient']['ID']))
    else:
        update_session(cursor, "patient", f'SELECT * FROM patients WHERE ID = {patient_id}')
        patient_form = PatientForm(data=session['patient'])
        cursor.execute(f"SELECT * FROM addresses WHERE ID = {session['patient']['address_ID']}")
        address = cursor.fetchone()
        address_form = AddressForm(data=address)
        cursor.close()
        conn.close()
        return render_template("patientEditPage.html",
                            index=index,
                            clinique=session["clinique"],
                            optometriste=session["user"],
                            patient=session["patient"],
                            patient_form=patient_form,
                            address_form=address_form)
    

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
    patient_form = PatientForm()
    address_form = AddressForm()
    if request.method == 'POST' and patient_form.validate_on_submit() and address_form.validate_on_submit():
        try :
            new_address_data = {
                'street_number': address_form.street_number.data,
                'street_name': address_form.street_name.data,
                'city': address_form.city.data,
                'province': address_form.province.data,
                'postal_code': address_form.postal_code.data,
            }

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            sql_insert_address_query = "INSERT INTO addresses (street_number, street_name, city, province, postal_code) VALUES (%s, %s, %s, %s, %s)"
            params = tuple(new_address_data.values())
            cursor.execute(sql_insert_address_query, params)
            conn.commit()

            new_address_id = cursor.lastrowid

            new_patient_data = {
                'first_name': patient_form.first_name.data,
                'last_name': patient_form.last_name.data,
                'birth_date': patient_form.birth_date.data,
                'gender': patient_form.gender.data,
                'email': patient_form.email.data,
                'phone_number': patient_form.phone_number.data,
                'RAMQ_number': patient_form.RAMQ_number.data,
                'address_ID': new_address_id
            }

            sql_insert_patient_query = "INSERT INTO patients (first_name, last_name, birth_date, gender, email, phone_number, RAMQ_number, address_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
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
                patient_form=patient_form,
                address_form=address_form)

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
            patient_form=patient_form,
            address_form=address_form)
    except Error as e:
        print(f"Error with MySQL: {e}")