from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo
from layouts.examples_page_layout import example_navbar, examples_main


##==================================
## Assemble layout
##==================================
out = [
    example_navbar.get(),
    html.Br(),
    examples_main.get()
]

def layout():
    return out
