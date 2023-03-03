import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo
from layouts.home_layout import home_navbar, password_entry

##==================================
## Welcome message
##==================================
welcome = dbc.Col(
    html.H2(['Welcome to Wiz!'], style = dict(textAlign='center')),
    width = dict(size = 8, offset = 2),
)

##==================================
## Assemble layout
##==================================
out = [
    home_navbar.get(),
    html.Br(),
    welcome,
    html.Br(),
    html.Br(),
    password_entry.get(),
]

def layout():
    return out
