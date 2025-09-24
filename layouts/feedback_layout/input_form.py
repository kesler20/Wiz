from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

##==================================
## Feedback Form
##==================================
form = dbc.Col(
    dbc.FormGroup([
        html.H5('Fill out the form and we will get back to you as soon as we can.', style = dict(textAlign='center')),
        html.Br(),
        html.H6('First Name:'),
        dbc.Input(type="text", placeholder="First Name", bs_size="md", id = 'feedback-fname'),
        html.Br(),
        html.H6('Last Name:'),
        dbc.Input(type="text", placeholder="Last Name", bs_size="md",id = 'feedback-lname'),
        html.Br(),
        html.H6('Email:'),
        dbc.Input(type="email", placeholder="example@shef.ac.uk", bs_size="md",id = 'feedback-email'),
        html.Br(),
        html.H6('Purpose for contact:'),
        dbc.RadioItems(
            options=[
                {"label": "Bug Reporting", "value": 1},
                {"label": "Help with Using Wiz", "value": 2},
                {"label": "Feature Suggestions", "value": 3},
                {"label": "Other", "value": 4},
            ],
            value=1,
            inline=True,
            id='feedback-radio'
        ),
        html.Br(),
        html.H6('Message:'),
        dbc.Textarea(bs_size = 'md', placeholder="Enter text here ...", id = 'feedback-text'),
        html.Br(),
        html.Br(),

        dbc.Button("Submit", color="primary", id = 'feedback-submit',href='/contact-us-confirm'),

    ]),
    width = dict(size = 8, offset = 2),
)


def get():
    return form
