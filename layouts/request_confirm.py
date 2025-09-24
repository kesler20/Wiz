from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo
from layouts.request_confirm_layout import confirm_navbar

##==================================
## Text
##==================================
text = dbc.Col(
    [
        html.H3('Thanks for requesting a password!'),
        html.H5('You will receive an email response soon.'),
        html.Br(),
        html.H5(
            [
                'Until then, check out some ',
                dcc.Link('examples', href='/examples'),
                ' of the ways Wiz can be used with your data!'
            ]
        ),
    ],
    style = dict(textAlign='center'),
    width = dict(size = 8, offset = 2),
)

##==================================
## Assemble layout
##==================================

out = [
    confirm_navbar.get(),
    html.Br(),
    text
]

def layout():
    return out
