import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from app import app


# Store the password entered
@app.callback(
        Output('password-store', 'value'),
    [
        Input('password-submit','n_clicks'),
    ],
    [
        State('password-enter','value')
    ]
)
def get_password_result(n_clicks, password_attempt):
    CORRECT_PASSWORD = 'wiz2020'
    if password_attempt == CORRECT_PASSWORD:
        output = 'correct'
    elif password_attempt == None:
        output = None
    else:
        output = 'incorrect'
    return output

# Verify password
@app.callback(
        Output('password-enter','invalid'),
    [
        Input('password-store', 'value')
    ]
)
def invalid_password(password_attempt):
    if password_attempt == 'incorrect':
        output = True
    else:
        output = False
    return output
