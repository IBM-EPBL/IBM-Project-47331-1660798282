import numpy as np
import pickle
from flask import request, render_template,Flask,redirect,url_for
from flask_cors import CORS
import joblib

app = Flask(__name__, static_url_path='')
CORS(app)
model = pickle.load(open('model.pkl', 'rb')) 

@app.route('/')
def sendHomePage():
    return render_template('sample.html')
    
@app.route('/predict')
def predictSpecies():
    return render_template('predict.html')

@app.route('/result',methods=['POST','GET'])
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
    va = [[Age, Gender, Total_Bilirubin, Direct_Bilirubin, Alkaline_Phosphotase, Alamine_Aminotransferase, Aspartate_Aminotransferase, Total_Protiens, Albumin, Albumin_and_Globulin_Ratio ]]
    
    prediction = model.predict(va)[0]

    if prediction==1:
        return render_template('negative.html',predict=prediction)
    else:
        return render_template('positive.html',predict=prediction)                

if __name__ == '__main__':
    app.run(debug=True)
