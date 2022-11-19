import requests

import flask
from flask import request, render_template
from flask_cors import CORS


# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "JAxHcDVDwZ4Shfl8HYp9TcCXBQG7CGEIFPz0Pa1y0jVu"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}


app = flask.Flask(__name__, static_url_path='')
CORS(app)
@app.route('/', methods=['GET','POST'])
def sendHomePage():
    return render_template('sample.html')
 
@app.route('/predict', methods=['GET'])
def predictSpecies():
    return render_template('predict.html')

@app.route('/result', methods=['POST','GET'])
def result():
    Age = int(request.form['Age'])
    Gender = int(request.form['Gender'])
    Total_Bilirubin = float(request.form['Total_Bilirubin'])
    Direct_Bilirubin = float(request.form['Direct_Bilirubin'])
    Alkaline_Phosphotase = int(request.form['Alkaline_Phosphotase'])
    Alamine_Aminotransferase = int(request.form['Alamine_Aminotransferase'])
    Aspartate_Aminotransferase = int(request.form['Aspartate_Aminotransferase'])
    Total_Protiens = float(request.form['Total_Protiens'])
    Albumin = float(request.form['Albumin'])
    Albumin_and_Globulin_Ratio = float(request.form['Albumin_and_Globulin_Ratio'])
    X = [[Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio ]]
   
   # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"fields": ["Age","Gender","Total_Bilirubin","Direct_Bilirubin","Alkaline_Phosphotase","Alamine_Aminotransferase","Aspartate_Aminotransferase","Total_Protiens","Albumin","Albumin_and_Globulin_Ratio"], "values":X}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/a4fa3d2d-3abc-4489-8c70-b8cdf7c06949/predictions?version=2022-11-11', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    predictions = response_scoring.json()
    predict = predictions['predictions'][0]['values'][0][0]
    confidence = (predictions['predictions'][0]['values'][0][1][1]) * 100
    # showing the prediction results in a UI# showing the prediction results in a UI
    if predict==1:
        return render_template('negative.html')
    else:
        return render_template('positive.html',confidence=confidence)

if __name__ == '__main__' :
    app.run(debug= True)

