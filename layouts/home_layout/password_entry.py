from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

##==================================
## Enter password
##==================================
password_form = dbc.Col(
    dbc.FormGroup([
        html.H5('To use Wiz, please submit a password...'),
        dbc.Row([
            dbc.Col(
                dbc.Input(type="password", placeholder="Enter password", persistence = True, bs_size="lg",id="password-enter"),
                style = dict(display = 'inline-block'),
                width = dict(size = 10, offset = 0),
            ),
            dbc.Col(
                dbc.Button("Submit", color="primary", id="password-submit"),
                style = dict(display = 'inline-block'),
                width = dict(size = 2, offset = 0),
                align = "center"
            )
        ], style = dict(verticalAlign = 'middle')
        ),
        html.H6(
            ["If you don't have a password or yours is expired, then you must ",
            dcc.Link('request a password', href='/request-password'),
            ],
            style = dict(color = 'secondary')
        ),
    ]),
    width = dict(size = 8, offset = 2),
)

def get():
    return password_form
