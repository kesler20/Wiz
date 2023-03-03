import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo
from layouts.help_layout import navbar, getting_started


##==================================
## Assemble layout
##==================================
out = [
    navbar.get(),
    getting_started.get()
]

def layout():
    return out
