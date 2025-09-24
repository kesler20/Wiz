from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo
from layouts.loading_layout import navbar

##==================================
## Assemble layout
##==================================
out = [
    navbar.get(),
    html.Br(),
    dbc.Col(
        dbc.Spinner(color='primary', size = 'lg'),
        style = dict(textAlign = 'center')
    )
]

def layout():
    return out
