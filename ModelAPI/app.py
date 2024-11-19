from flask import Flask, request, jsonify
import pickle
from sklearn.preprocessing import StandardScaler
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# Original Code: env variable inserted into running container using AWS Secrets in runtime.
#PREDICT_API_KEY = os.getenv("PREDICT_API_KEY") 

# For Interview Purpose:
PREDICT_API_KEY = "18347531767fe7fcf5a92f407df6355df07ddfd5517564de938a5f33bd181d99"

if not PREDICT_API_KEY:
    raise RuntimeError("API key not set. Ensure the PREDICT_API_KEY environment variable is configured.")


def preprocess_input(data):
    Education = data["Education"]
    ApplicantIncome = data["ApplicantIncome"]
    Coapplicant = data["Co-applicant"]
    LoanAmount = data["LoanAmount"]
    LoanAmountTerm = data["Loan-Amount-Term"]
    CreditHistory = data["Credit-History"]
    dependents = data["dependents"]
    property = data["property"]

    se = 0 if Education == "Graduate" else 1

    if dependents == "0":
        s1, s2, s3, s4 = 0, 0, 0, 1
    elif dependents == "1":
        s1, s2, s3, s4 = 0, 0, 1, 0
    elif dependents == "2":
        s1, s2, s3, s4 = 0, 1, 0, 0
    elif dependents == "3+":
        s1, s2, s3, s4 = 1, 0, 0, 0
    else:
        raise ValueError("Invalid dependents value")

    if property == "Rural":
        sp1, sp2, sp3 = 0, 0, 1
    elif property == "Semi-urban":
        sp1, sp2, sp3 = 0, 1, 0
    elif property == "Urban":
        sp1, sp2, sp3 = 1, 0, 0
    else:
        raise ValueError("Invalid property value")
    arrayofinputs = [[
        float(se), float(ApplicantIncome), float(Coapplicant),
        float(LoanAmount), float(LoanAmountTerm), float(CreditHistory),
        float(s1), float(s2), float(s3), float(s4),
        float(sp1), float(sp2), float(sp3)
    ]]
    return arrayofinputs

@app.route('/predict', methods=['POST'])
def predict():
    try:
        api_key = request.headers.get("x-api-key")
        if api_key != PREDICT_API_KEY:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        inputs = preprocess_input(data)
        scaled_inputs = scaler.transform(inputs)
        prediction = model.predict(scaled_inputs)
        result = {'status': 'approved' if prediction[0] == 1 else 'rejected'}

        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)