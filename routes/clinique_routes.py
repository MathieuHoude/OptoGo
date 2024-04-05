from flask import render_template, request, redirect, url_for, session, Blueprint
import os
import mysql.connector
from mysql.connector import Error
import bcrypt

cliniques_bp = Blueprint('cliniques', __name__, url_prefix='/cliniques')
from DB.utils import get_db_connection
from utils import update_session

# route pour la liste des patients d'une clinique
@cliniques_bp.route("/<clinique_id>")
def clinique(clinique_id):
    """
    This function retrieves the details of a specific clinic and its associated patients.

    :param clinique_id: The unique identifier of the clinic to retrieve.
    :type clinique_id: int
    :return: A rendered HTML template containing the clinic details and its patients.
    """
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
@cliniques_bp.route("<int:clinique_id>/patients/<int:patient_id>")
def choice(clinique_id, patient_id):
    """
    This function renders the "choicePage.html" template with the selected clinic and patient details.

    :param clinique_id: The unique identifier of the clinic to retrieve.
    :type clinique_id: int
    :param patient_id: The unique identifier of the patient to retrieve.
    :type patient_id: int
    :return: A rendered HTML template containing the selected clinic and patient details.
    """
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


