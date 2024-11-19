from os import stat
import requests
from flask import Flask, render_template, request, url_for, redirect, jsonify

API_KEYS = {
    "/predict": "18347531767fe7fcf5a92f407df6355df07ddfd5517564de938a5f33bd181d99",
    "/setModelURL": "d3baa33ef55ec43a11318cd96f7442622d6753f92b7ef06b0b9efde27c3062ac"
}

# Default model URL (this will be updated with /setPredictURL)
model_url = "http://18.190.157.32:5000/predict"

app = Flask(__name__)

@app.route('/')
def loadhome():
    return render_template("homepage.html")


@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template("prediction.html")


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    return redirect(url_for('form'))


@app.route('/submit', methods=['POST'])  # url binding
def user():
    Education = request.form["Education"]
    ApplicantIncome = request.form["ApplicantIncome"]
    Coapplicant = request.form["Co-applicant"]
    LoanAmount = request.form["LoanAmount"]
    LoanAmountTerm = request.form["Loan-Amount-Term"]
    CreditHistory = request.form["Credit-History"]
    dependents = request.form["dependents"]
    property = request.form["property"]

    input_data = {
        "Education": Education,
        "ApplicantIncome": ApplicantIncome,
        "Co-applicant": Coapplicant,
        "LoanAmount": LoanAmount,
        "Loan-Amount-Term": LoanAmountTerm,
        "Credit-History": CreditHistory,
        "dependents": dependents,
        "property": property
    }

    # Call the model's /predict API
    headers = {'x-api-key': API_KEYS["/predict"]}
    try:
        response = requests.post(model_url, json=input_data, headers=headers)
        prediction = response.json().get('status', 'error')

        if response.status_code == 200:
            return render_template("result.html", output=f"Prediction: {prediction}")
        else:
            return render_template("error.html", error_message="Something went wrong. Please try again later.")
    except Exception as e:
        return render_template("error.html", error_message=f"Something went wrong. Please try again later.")


@app.route('/setPredictURL', methods=['POST'])
def set_predict_url():
    api_key = request.headers.get("x-api-key")
    
    if api_key != API_KEYS["/setModelURL"]:
        return jsonify({'error': 'Unauthorized'}), 401

    new_model_url = request.json.get("model_url")
    if not new_model_url:
        return jsonify({'error': 'Model URL not provided'}), 400

    global model_url
    model_url = new_model_url
    return jsonify({"status": "Model URL updated successfully"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
