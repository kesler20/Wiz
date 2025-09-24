from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo
from layouts.home_layout import home_navbar

##==================================
## Welcome message
##==================================
message = dbc.Col(
    html.H3(['No page here! Please return to the ', dcc.Link('homepage.', href = '/')], style = dict(textAlign='center')),
    width = dict(size = 8, offset = 2),
)

##==================================
## Assemble layout
##==================================
out = [
    home_navbar.get(),
    html.Br(),
    message,
]

def layout():
    return out
