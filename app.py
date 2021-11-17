import flask
import pandas as pd
from joblib import dump, load


with open(f'pipeline.joblib', 'rb') as f:
    model = load(f)


app = flask.Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET', 'POST'])
def main():
    if flask.request.method == 'GET':
        return (flask.render_template('main.html'))

    if flask.request.method == 'POST':
        Gender = flask.request.form['Gender']
        Married = flask.request.form['Married']
        Dependents = flask.request.form['Dependents']
        Education = flask.request.form['Education']
        Self_Employed = flask.request.form['Self_Employed']
        ApplicantIncome = flask.request.form['ApplicantIncome']
        CoapplicantIncome = flask.request.form['CoapplicantIncome']
        Credit_History = flask.request.form['Credit_History']


        input_variables = pd.DataFrame([[Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoapplicantIncome, Credit_History]],
                                       columns=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
                                                'ApplicantIncome', 'CoapplicantIncome', 'Credit_History'],
                                                index=['input'])

        predictions = model.predict(input_variables)[0]
        print(predictions)

        return flask.render_template('main.html', 
                                      original_input={
                                        'Gender': Gender,
                                        'Married': Married, 
                                        'Dependents': Dependents, 
                                        'Education': Education, 
                                        'Self_Employed': Self_Employed, 
                                        'ApplicantIncome': ApplicantIncome, 
                                        'CoapplicantIncome': CoapplicantIncome, 
                                        'Credit_History': Credit_History},
                                        result=predictions)


if __name__ == '__main__':
    app.run(debug=True)