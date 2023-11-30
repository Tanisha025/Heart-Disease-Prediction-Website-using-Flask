from flask import Flask, render_template, request
import pickle

app = Flask(__name__, static_url_path='/static')
# load the model
model = pickle.load(open('savedmodel.sav', 'rb'))

@app.route('/')
def home():
    result = ''
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/preventions')
def preventions():
    return render_template('preventions.html')

@app.route('/symptoms')
def symptoms():
    return render_template('symptoms.html')

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    sysBP = float(request.form['sysBP'])
    glucose = float(request.form['glucose'])
    age = int(request.form['age'])
    cigsPerDay = float(request.form['cigsPerDay'])
    totChol = float(request.form['totChol'])
    diaBP = float(request.form['diaBP'])
    prevalentHyp = int(request.form['prevalentHyp'])
    male = int(request.form['male'])
    BPMeds = float(request.form['BPMeds'])
    diabetes = int(request.form['diabetes'])

    # Assuming your model provides probabilities using predict_proba
    probabilities = model.predict_proba([[sysBP, glucose, age, cigsPerDay, totChol, diaBP, prevalentHyp, male, BPMeds, diabetes,]])[0]
    result = model.predict([[sysBP, glucose, age, cigsPerDay, totChol, diaBP, prevalentHyp, male, BPMeds, diabetes,]])[0]

    # Extract probability of class 1 (heart disease)
    probability_heart_disease = round(probabilities[1], 2)

    if result == 1:
        result_message = "Chances of Heart Disease: High "
    else:
        result_message = "Chances of Heart Disease: Low "

    return render_template('index.html', result=result_message, probability=probability_heart_disease)

if __name__ == '__main__':
    app.run(debug=True)