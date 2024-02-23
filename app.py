from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ClinicGlobal = {"clinique": ""}

OptoInfoGLobal = {
    "PracticeNumber": '123456',
    "Adresse": '2250 rue Sicard',
    "Phone": '4508480147'
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


@app.route("/patients")
def patients():
    index = 2
    return render_template("patientPage.html", index=index, ClinicGlobal=ClinicGlobal["clinique"])


@app.route("/update_clinic", methods=["GET"])
def update_clinic():
    selected_option = request.args.get("selected_option")
    ClinicGlobal["clinique"] = selected_option
    response_data = {"message": "Option sélectionnée : " + selected_option}
    return jsonify(response_data)


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



if __name__ == '__main__':
    app.run(debug=True)
