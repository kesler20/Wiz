from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo
from layouts.feedback_layout import feedback_navbar, input_form

##==================================
## Welcome message
##==================================
welcome = dbc.Col(
    html.H3(['Contact Us'], style = dict(textAlign='center')),
    width = dict(size = 8, offset = 2),
)

##==================================
## Assemble layout
##==================================

out = [
    feedback_navbar.get(),
    html.Br(),
    welcome,
    html.Br(),
    html.Br(),
    input_form.get(),
]

def layout():
    return out
