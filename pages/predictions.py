# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pickle
# Imports from this application
from app import app


pickin = open('pages/pipeline.p','rb')
pipeline = pickle.load(pickin)
# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [   
        # Contains the header, sub header and question Number 1
        dcc.Markdown(
            """
            #df
            ## Pre-Approval Appilication
            Please enter the informaiton below.


            #### 1. Are you Male or Female?

            """
        ),

        dcc.Dropdown(
        id='Gender',
        options=[
            {'label': 'Male', 'value': 1},
            {'label': 'Female', 'value': 0},
        ],
        value=1
        ),

        # Question 2.
        dcc.Markdown(
            """
            #### 2. Are you Married?
            """
        ),

        dcc.Dropdown(
        id='Married',
        options=[
            {'label': 'Yes', 'value': 1},
            {'label': 'No', 'value': 0},
        ],
        value=1
        ),

        #question 3
        dcc.Markdown(
            """
            #### 3. Do you have any dependents?
            """
        ),

        dcc.Dropdown(
        id='Dependents',
        options=[
            {'label': '0', 'value': 0},
            {'label': '1', 'value': 1},
            {'label': '2', 'value': 2},
            {'label': '3+', 'value': 3},
        ],
        value=0
        ),


        #question 4
        dcc.Markdown(
            """
            #### 4. Have you graduated?
            """
        ),

        dcc.Dropdown(
        id='Education',
        options=[
            {'label': 'Yes', 'value': 1},
            {'label': 'No', 'value': 0},
        ],
        value=0
        ),


        #question 5
        dcc.Markdown(
            """
            #### 5. Are you self-employed
            """
        ),

        dcc.Dropdown(
        id='Self_Employed',
        options=[
            {'label': 'Yes', 'value': 1},
            {'label': 'No', 'value': 0},

        ],
        value=0
        ),


        dcc.Markdown(
            """
            #### 6. Enter your Monthly Income
            """
        ),

        # Question 6
        dcc.Input(
            id="ApplicantIncome",
            type='number',
            placeholder="Input Amount Here",
        ),
        
        
        
        # Co App INcome
        dcc.Markdown(
            """
            #### 7. Co-Applicant Monthly Income
            If you don't have a Co-Appilicant. Enter 0
            """
        ),

        # Question 7
        dcc.Input(
            id="CoApplicantIncome",
            type='number',
            placeholder="Input Amount Here",
        ),

        #question 8
        dcc.Markdown(
            """
            #### 8. Credit Score
            """
        ),

        dcc.Dropdown(
        id='Credit_History',
        options=[
            {'label': '300-579', 'value': 0},
            {'label': '580+', 'value': 1},

        ],
        value=0
        ),
    ],
    md=4,
)

column2 = dbc.Col(
    [
    html.H2('Results', className='mb-5'),
    html.Div(id='Approval', className='lead')


    ]
)

layout = dbc.Row([column1, column2])

@app.callback(
    Output(component_id='Approval', component_property='children'),
    [
    Input(component_id='Gender', component_property='value'),
    Input(component_id='Married', component_property='value'),
    Input(component_id='Dependents', component_property='value'),
    Input(component_id='Education', component_property='value'),
    Input(component_id='Self_Employed', component_property='value'),
    Input(component_id='ApplicantIncome', component_property='value'),
    Input(component_id='CoApplicantIncome', component_property='value'),
    Input(component_id='Credit_History', component_property='value'),
    ]
)


def predict(Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoApplicantIncome,Credit_History):
    dft = pd.DataFrame(
        columns=['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome','Credit_History'],
        data=[[Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome, CoApplicantIncome,Credit_History]]
    )
    y_pred = pipeline.predict(dft)[0]
    print(y_pred)
    if y_pred == 0:
        return 'You are not Pre-Approved'
    else:
        return 'You are Pre-Approved'
