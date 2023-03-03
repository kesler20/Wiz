import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo
from layouts.request_password_layout import rp_navbar, input_form

##==================================
## Welcome message
##==================================
welcome = dbc.Col(
    html.H3(['Request Password'], style = dict(textAlign='center')),
    width = dict(size = 8, offset = 2),
)

##==================================
## Assemble layout
##==================================

out = [
    rp_navbar.get(),
    html.Br(),
    welcome,
    html.Br(),
    html.Br(),
    input_form.get(),
]

def layout():
    return out
