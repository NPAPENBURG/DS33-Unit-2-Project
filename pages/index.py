# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(
            """
        
            ## First Step Towards Your Dream Home!

            If you have ever wonder to yourself how to go about getting your dream home. This is the appilcation for you!

            This appilcation will help you with prediciting if you will be pre-approved for a home loan!

            Take the first step and apply by clicking the Apply button below!

            """
        ),
        dcc.Link(dbc.Button('Apply!', color='primary'), href='/predictions')
    ],
    md=4,
)

gapminder = px.data.gapminder()
fig = px.scatter(gapminder.query("year==2007"), x="gdpPercap", y="lifeExp", size="pop", color="continent",
           hover_name="country", log_x=True, size_max=60)

column2 = dbc.Col(
    [

    ]
)

layout = dbc.Row([column1, column2])