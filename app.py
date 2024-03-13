from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ClinicGlobal = {"clinique": ""}

# Dico en exemple d'infos opto
OptoInfoGLobal = {
    "PracticeNumber": '123456',
    "Adresse": '2250 rue Sicard',
    "Phone": '4508480147'
}

# Dico en exemple de patient
PatientSelect = {
    "first_name": 'Jeremy',
    "last_name": 'Maitre',
    "email": 'ggmaitre@gmail.com',
    "phone": '4508480147',
    "gender": 'Homme',
    "birthDate": '02/07/1991',
    "ramq": "JEMAI XXXX XXXX XXXX"
}


@app.route("/")
@app.route("/index")
def index():
    index = 1
    return render_template(
        "index.html",
        index=index,
        PracticeNumber=OptoInfoGLobal["PracticeNumber"],
        Adresse=OptoInfoGLobal["Adresse"],
        Phone=OptoInfoGLobal["Phone"]
    )


# route pour la page du patient
@app.route("/patients")
def patients():
    index = 2
    return render_template("patientPage.html",
                           index=index,
                           ClinicGlobal=ClinicGlobal["clinique"],
                           Patient=PatientSelect)


# route pour la page des cards de choix
@app.route("/choice")
def choice():
    index = 3
    return render_template("choicePage.html",
                           index=index,
                           ClinicGlobal=ClinicGlobal["clinique"],
                           Patient=PatientSelect)


# route pour la page des informations du patient
@app.route("/patient-information")
def patient_information():
    index = 4
    return render_template("patientInformationPage.html",
                           index=index,
                           ClinicGlobal=ClinicGlobal["clinique"],
                           Patient=PatientSelect
                           )


# route pour la page d'un nouvel examen
@app.route("/patient-exam")
def patient_exam():
    index = 5
    return render_template("newExamPage.html",
                           index=index,
                           ClinicGlobal=ClinicGlobal["clinique"],
                           Patient=PatientSelect
                           )


# route pour la page d'un nouvel examen
@app.route("/login")
def login():
    return render_template("loginPage.html")


# gestion de la requete HTTP pour mettre a jour la clinique
@app.route("/update_clinic", methods=["GET"])
def update_clinic():
    selected_option = request.args.get("selected_option")
    ClinicGlobal["clinique"] = selected_option
    response_data = {"message": "Option sélectionnée : " + selected_option}
    return jsonify(response_data)


# gestion de la requete HTTP pour mettre a jour les infos de l'opto
@app.route("/update_opto", methods=["GET"])
def update_opto():
    new_practice_number = request.args.get("practice_number")
    new_adresse = request.args.get("adresse")
    new_phone_number = request.args.get("phone_number")
    OptoInfoGLobal["PracticeNumber"] = new_practice_number
    OptoInfoGLobal["Adresse"] = new_adresse
    OptoInfoGLobal["Phone"] = new_phone_number
    response_data = {"message": "Informations de l'optométriste mises à jour avec succès"}
    return jsonify(response_data)


# gestion de la requete HTTP pour selectionner le patient depuis la page patientsTable.html
@app.route("/select_patient", methods=["GET"])
def select_patient():
    selected_option = request.args.get("selected_patient")
    PatientSelect["name"] = selected_option
    response_data = {"message": "Option sélectionnée : " + selected_option}
    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
