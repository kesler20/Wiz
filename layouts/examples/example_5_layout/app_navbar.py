from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

##==================================
## Navigation bar
##==================================
download_link = html.A(
    'Download Plot Data',
    id = 'example-5-download-link',
    download = 'data.csv',
    href = '',
    target = '_blank',
    style = dict(color = 'white'),
    className= 'downloadlink'
),

navbar = dbc.NavbarSimple(
    [
        dbc.Nav(
            dbc.Row(
                [
                    dbc.NavItem(dbc.NavLink(download_link),id='example-5-dowload-nav'),
                    dbc.NavItem(dbc.NavLink('Home',href = '/')),
                    dbc.NavItem(dbc.NavLink('Examples',href = '/examples')),
                    dbc.NavItem(dbc.NavLink('Help/Documentation', href='/help')),
                    dbc.NavItem(dbc.NavLink('Contact Us', href='/contact-us')),
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
