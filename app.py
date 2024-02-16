from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

ClinicGlobal = {}


@app.route("/")
@app.route("/index")
def index():
    index = 1
    return render_template("index.html", index=index)


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


if __name__ == '__main__':
    app.run(debug=True)