from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

##==================================
## Input Form
##==================================
form = dbc.Col(
    dbc.FormGroup([
        html.H5('Fill in the form and a password will be emailed to you.', style = dict(textAlign='center')),
        html.Br(),
        html.H6('First Name:'),
        dbc.Input(type="text", placeholder="Earl", bs_size="md", id = 'rp-fname'),
        html.Br(),
        html.H6('Last Name:'),
        dbc.Input(type="text", placeholder="Grey", bs_size="md",id = 'rp-lname'),
        html.Br(),
        html.H6('Email:'),
        dbc.Input(type="email", placeholder="example@shef.ac.uk", bs_size="md",id = 'rp-email'),
        html.Br(),
        html.H6('Purpose for use'),
        dbc.RadioItems(
            options=[
                {"label": "Academia", "value": 1},
                {"label": "Industrial", "value": 2},
                {"label": "Other", "value": 3},
            ],
            value=1,
            inline=True,
            id='rp-radio'
        ),
        html.Br(),
        html.Br(),

        dbc.Button("Request Password", color="primary", id = 'rp-submit',href='/request-confirm'),

    ]),
    width = dict(size = 8, offset = 2),
)


def get():
    return form
