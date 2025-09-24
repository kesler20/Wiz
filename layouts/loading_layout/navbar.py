from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

##==================================
## Navigation bar
##==================================
navbar = dbc.NavbarSimple(
    [
        dbc.Nav(
            dbc.Row(
                [
                    # Navigation
                    dbc.NavItem(dbc.NavLink('Help/Documentation', href='/help')),
                    dbc.NavItem(dbc.NavLink('Examples', href='/examples')),
                 ],
                 align="center",
                 no_gutters=True,
            ),
        fill = True
        ),
    ],
    brand='  ',
    brand_href="#",
    color="primary",
    id='navBar',
    light = False,
    dark = True,
)

def get():
    return navbar
