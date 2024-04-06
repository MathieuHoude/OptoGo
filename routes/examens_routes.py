from flask import render_template, request, redirect, url_for, session, Blueprint
from mysql.connector import Error
import json

from forms.exam_form import ExamForm
from forms.histoireDeCas_form import HistoireDeCasForm
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
        update_session(cursor, "examen", f"SELECT * FROM examens e WHERE e.ID = {examen_id}")
        cursor.execute(f"SELECT * FROM histoireDeCas h WHERE h.ID = {session['examen']['histoireDeCas_ID']}")
        hdc = cursor.fetchone()
        conn.close()
        session["examen"] = parse_json_objects(session["examen"])
        hdc = parse_json_objects(hdc)
        exam_form = ExamForm(data=session["examen"])
        hdc_form = HistoireDeCasForm(data=hdc)
        confirmation_message = session.pop('confirmation_message', None)
        return render_template("examDetailsPage.html",
                            index=index,
                            clinique=session["clinique"],
                            optometriste=session["user"],
                            patient=session["patient"],
                            examen=session["examen"],
                            confirmation_message=confirmation_message,
                            exam_form=exam_form,
                            hdc_form=hdc_form
                            )
    except Error as e:
        print(f"Error connecting to MySQL: {e}")



# route pour la page d'un nouvel examen
@examens_bp.route("/new", methods=['GET', 'POST'])
def new():
    try:
        index = 5
        clinique_id = request.args.get('clinique_id')
        patient_id = request.args.get('patient_id')
        confirmation_message = session.pop('confirmation_message', None)
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        update_session(cursor, "clinique", f"SELECT * FROM cliniques WHERE ID = {clinique_id}")
        update_session(cursor, "patient", f"SELECT * FROM patients WHERE ID = {patient_id}")
        if 'examen' in session: session.pop('examen', None) 
        exam_form = ExamForm()
        if 'histoireDeCas_ID' in session:
            cursor.execute(f"SELECT * FROM histoireDeCas WHERE ID = {session.pop('histoireDeCas_ID', None)}")
            hdc = cursor.fetchone()
            session['histoireDeCas'] = parse_json_objects(hdc)
            hdc_form = HistoireDeCasForm(data=session['histoireDeCas'])
        elif 'histoireDeCas' in session:
            hdc_form = HistoireDeCasForm(data=session['histoireDeCas'])
        else: 
            hdc_form = HistoireDeCasForm()
        conn.close()
        return render_template("newExamPage.html",
                            index=index,
                            clinique=session['clinique'],
                            optometriste=session["user"],
                            patient=session['patient'],
                            confirmation_message=confirmation_message,
                            exam_form=exam_form,
                            hdc_form=hdc_form
                            )
    except Error as e:
        print(f"MySQL error: {e}")

@examens_bp.route("/<int:examen_id>/prescription")
def prescription(examen_id):
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
        session["examen"] = parse_json_objects(session["examen"])
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

# route pour sauvegarder l'histoire de cas
@examens_bp.route("/submit_histoireDeCas", methods=['POST'])
def submit_histoireDeCas():
    index = 5
    form = HistoireDeCasForm()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if form.validate_on_submit():
        histoireDeCas_data = build_histoireDeCas_data(form)
       
        # Convert each sub-dictionary to JSON strings
        for key, value in histoireDeCas_data.items():
            if type(value) == dict:
                try:
                    histoireDeCas_data[key] = json.dumps(value)
                except (json.JSONDecodeError, TypeError):
                    pass
        if form.ID.data: #Existing hdc
            # cursor.execute(f'SELECT * FROM histoireDeCas WHERE ID = {form.ID.data}')
            # hdc = cursor.fetchone()
            # modified_fields = {}
            # for field in form: 
            #     if field.name != 'csrf_token' and field.data != hdc[field.name]:
            #         modified_fields[field.name] = field.data

            # if modified_fields:
            #     sql_update_query = "UPDATE histoireDeCas SET "
            #     sql_update_query += ", ".join([f"{field} = %s" for field in modified_fields.keys()])
            #     sql_update_query += " WHERE id = %s"
                
            #     # Create a tuple of parameter values in the same order as placeholders
            sql_query = "UPDATE histoireDeCas SET conditions = %s, allergies = %s, medications = %s, trouble_vision = %s, antecedants_familiaux = %s, antecedants_oculaires = %s, notes = %s WHERE ID = %s"
            params = tuple(histoireDeCas_data.values()) + (form.ID.data,)
            cursor.execute(sql_query, params)
            conn.commit()
            session['histoireDeCas_ID'] = form.ID.data
        else: #New hdc
            sql_query = "INSERT INTO histoireDeCas (conditions, allergies, medications, trouble_vision, antecedants_familiaux, antecedants_oculaires, notes) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            params = tuple(histoireDeCas_data.values())
            cursor.execute(sql_query, params)
            conn.commit()
            session['histoireDeCas_ID'] = cursor.lastrowid
        cursor.close()
        conn.close()
        session['confirmation_message'] = {"title": "Histoire de cas sauvegardée", "text": f"L'histoire de cas de l'examen en cours a été sauvegardée avec succès."}
        if form.ID.data: #Existing hdc
            if 'examen' not in session: 
                return redirect(url_for("examens.new", clinique_id=f"{session['clinique']['ID']}", patient_id=f"{session['patient']['ID']}"))
            else:
                return redirect(url_for("examens.details",examen_id=f"{session['examen']['ID']}", clinique_id=f"{session['clinique']['ID']}", patient_id=f"{session['patient']['ID']}"))
        else: #New hdc
            return redirect(url_for("examens.new", clinique_id=f"{session['clinique']['ID']}", patient_id=f"{session['patient']['ID']}"))
    else:
        cursor.close()
        conn.close()
        return render_template("newExamPage.html",
                            index=index,
                            clinique=session['clinique'],
                            optometriste=session["user"],
                            patient=session['patient'],
                            hdc_form=form
                            )

@examens_bp.route("/submit_examen", methods=['POST'])
def submit_examen():
    index = 5
    form = ExamForm()
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    # if not validate_hidden_fields(session, form):
    #     session['error_message'] = {'title': "Erreur lors de la création de l'examen", 'message': "Vous avez soumis une valeur incorrecte"}
    #     if form.ID.data: #Existing exam
    #         return redirect(url_for("examens.details",examen_id=f"{session['examen']['ID']}", clinique_id=f"{session['clinique']['ID']}", patient_id=f"{session['patient']['ID']}"))
    #     else: #New exam
    #         return redirect(url_for("examens.new"))
    if request.method == 'POST' and form.validate_on_submit():
        new_exam_data = build_exam_data(form)
        cursor.execute(f'SELECT RX_subjective FROM examens e WHERE patient_ID = {form.patient_ID.data} ORDER BY created_at DESC LIMIT 1;')
        old_rx = cursor.fetchone()
        if old_rx:
            old_rx = parse_json_objects(old_rx) 
            new_exam_data['old_RX'] = {}
            for key, value in old_rx.items():
                # Replace the key name
                new_key = key.replace("RX_subjective_", "")
                new_exam_data['old_RX'][new_key] = value
        for key, value in new_exam_data.items():
            if type(value) == dict:
                try:
                    new_exam_data[key] = json.dumps(value)
                except (json.JSONDecodeError, TypeError):
                    pass
        if form.ID.data: #Existing exam
            if old_rx:
                sql_query = "UPDATE examens SET RX_objective = %s, RX_subjective = %s, contact_lens_type = %s, lens_type = %s, periode_validite = %s, patient_ID = %s, optometriste_ID = %s, histoireDeCas_ID = %s, old_RX = %s WHERE ID = %s"
            else:
                sql_query = "UPDATE examens SET RX_objective = %s, RX_subjective = %s, contact_lens_type = %s, lens_type = %s, periode_validite = %s, patient_ID = %s, optometriste_ID = %s, histoireDeCas_ID = %s WHERE ID = %s"
            params = tuple(new_exam_data.values()) + (form.ID.data,)
        else: #New exam
            sql_query = "INSERT INTO examens (RX_objective, RX_subjective, contact_lens_type, lens_type, old_RX, periode_validite, patient_ID, optometriste_ID, histoireDeCas_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            params = tuple(new_exam_data.values())
        cursor.execute(sql_query, params)
        conn.commit()
        cursor.close()
        conn.close()
        session['confirmation_message'] = {"title": "Examen sauvegardée", "text": f"L'examen en cours a été sauvegardé avec succès."}
        if form.ID.data: #Existing exam
            return redirect(url_for("examens.details",examen_id=f"{session['examen']['ID']}", clinique_id=f"{session['clinique']['ID']}", patient_id=f"{session['patient']['ID']}"))
        else: #New exam
            return redirect(url_for("examens.new",examen_id=f"{session['examen']['ID']}", clinique_id=f"{session['clinique']['ID']}", patient_id=f"{session['patient']['ID']}"))
    else:
        hdc_form = HistoireDeCasForm(data=session['histoireDeCas'])
        
        #SHOULD BE REDIRECT
        
        
        return render_template("newExamPage.html",
                        index=index,
                        clinique=session['clinique'],
                        optometriste=session["user"],
                        patient=session['patient'],
                        error_message={'title': "Erreur lors de la création de l'examen", 'message': "Vous avez soumis une valeur incorrecte"},
                        hdc_form=hdc_form,
                        exam_form=form
                        )     

def parse_json_objects(dict):
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
        except (json.JSONDecodeError, TypeError, AttributeError):
            # If parsing fails, simply copy the key-value pair to the new dictionary
            new_dict[key] = value
    
    return new_dict

def validate_hidden_fields(session, form):
    if form.patient_ID.data != session['patient']['ID']: return False
    if form.ID.data != session['examen']['ID']: return False
    # if form.examen_id.data != session['patient']['ID']: return False
    return True

def build_histoireDeCas_data(form):
     return  {
            'conditions': {
                "asthma": form.conditions_asthma.data, 
                "diabetes": form.conditions_diabetes.data,
                "cholesterol": form.conditions_cholesterol.data, 
                "hypertension": form.conditions_hypertension.data, 
                "heart_condition": form.conditions_heart_condition.data
            },
            'allergies': {
                "anesthetics": form.allergies_anesthetics.data, 
                "preservatives": form.allergies_preservatives.data, 
                "topical_antibiotics": form.allergies_topical_antibiotics.data, 
                "decongestant_eye_drops": form.allergies_decongestant_eye_drops.data, 
                "topical_corticosteroids": form.allergies_topical_corticosteroids.data
            },
            'medications': {
                "digoxin": form.medications_digoxin.data, 
                "amiodarone": form.medications_amiodarone.data, 
                "chloroquine": form.medications_chloroquine.data, 
                "isotretinoin": form.medications_isotretinoin.data, 
                "methylprednisolone": form.medications_methylprednisolone.data
            },
            'trouble_vision': {
                "flash": form.trouble_vision_flash.data, 
                "cataract": form.trouble_vision_cataract.data, 
                "floaters": form.trouble_vision_floaters.data, 
                "glaucoma": form.trouble_vision_glaucoma.data, 
                "strabismus": form.trouble_vision_strabismus.data, 
                "double_vision": form.trouble_vision_double_vision.data, 
                "macular_degeneration": form.trouble_vision_macular_degeneration.data
            },
            'antecedants_familiaux': {
                "glaucoma": form.antecedants_familiaux_glaucoma.data, 
                "retinal_detachment": form.antecedants_familiaux_retinal_detachment.data, 
                "macular_degeneration": form.antecedants_familiaux_macular_degeneration.data
            },
            'antecedants_oculaires': {
                "trauma": form.antecedants_oculaires_trauma.data, 
                "surgery": form.antecedants_oculaires_surgery.data, 
                "retinal_detachment": form.antecedants_oculaires_retinal_detachment.data
            },
            'notes': form.notes.data
        }

def build_exam_data(form):
    return {
            'RX_objective': {
                "Add_LE": form.RX_objective_Add_LE.data, 
                "Add_RE": form.RX_objective_Add_RE.data, 
                "Ast_LE": form.RX_objective_Ast_LE.data, 
                "Ast_RE": form.RX_objective_Ast_RE.data, 
                "Axis_LE": form.RX_objective_Axis_LE.data, 
                "Axis_RE": form.RX_objective_Axis_RE.data, 
                "Acuity_LE": form.RX_objective_Acuity_LE.data, 
                "Acuity_RE": form.RX_objective_Acuity_RE.data, 
                "Sphere_LE": form.RX_objective_Sphere_LE.data, 
                "Sphere_RE": form.RX_objective_Sphere_RE.data
            },
            'RX_subjective': {
                "Add_LE": form.RX_subjective_Add_LE.data, 
                "Add_RE": form.RX_subjective_Add_RE.data, 
                "Ast_LE": form.RX_subjective_Ast_LE.data, 
                "Ast_RE": form.RX_subjective_Ast_RE.data, 
                "Axis_LE": form.RX_subjective_Axis_LE.data, 
                "Axis_RE": form.RX_subjective_Axis_RE.data, 
                "Acuity_LE": form.RX_subjective_Acuity_LE.data, 
                "Acuity_RE": form.RX_subjective_Acuity_RE.data, 
                "Sphere_LE": form.RX_subjective_Sphere_LE.data, 
                "Sphere_RE": form.RX_subjective_Sphere_RE.data
            },
            'contact_lens_type': {
                "multifocal_contact_lenses": form.contact_lens_type_multifocal_contact_lenses.data, 
                "mono_vision_contact_lenses": form.contact_lens_type_mono_vision_contact_lenses.data, 
                "single_vision_contact_lenses": form.contact_lens_type_single_vision_contact_lenses.data
            },
            'lens_type': {
                "office_lenses": form.lens_type_office_lenses.data, 
                "bifocal_lenses": form.lens_type_bifocal_lenses.data, 
                "progressive_lenses": form.lens_type_progressive_lenses.data, 
                "single_vision_lenses": form.lens_type_single_vision_lenses.data
            },
            'periode_validite': form.periode_validite.data,
            'patient_ID': form.patient_ID.data,
            'optometriste_ID': form.optometriste_ID.data,
            'histoireDeCas_ID': form.histoireDeCas_ID.data,
        }