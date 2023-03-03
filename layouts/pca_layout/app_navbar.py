import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Navigation bar
##==================================
download_link = html.A(
    'Download Plot Data',
    id = 'pca-download-link',
    href = '',
    style = dict(color = 'white'),
    className= 'downloadlink'
),

navbar = dbc.NavbarSimple(
    [
        dbc.Nav(
            dbc.Row(
                [
                    dbc.NavItem(dbc.NavLink('Clear Data',id='clear-data-link',href='/temp-clear')),
                    dbc.NavItem(dbc.NavLink(download_link),id='pca-dowload-nav'),
                    dbc.NavItem(dbc.NavLink('Data Table',id='pca-table-open'), style = dict(cursor = 'pointer')),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem('Scatter', href="/"),
                            dbc.DropdownMenuItem('Lines', href="/lines"),
                        ],
                        label = "Plot Types",
                        nav = True,
                        id = 'pca-plot-types'
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem('Page Help', id='pca-help-open'),
                            dbc.DropdownMenuItem('Documentation', href='/help'),
                            dbc.DropdownMenuItem('Examples', href='/examples'),
                            dbc.DropdownMenuItem('Contact Us', href='/contact-us'),
                        ],
                        label = "Help",
                        nav = True,
                        in_navbar = True,
                        style = dict(marginRight = 50),
                        id = 'pca-help-dropdown'
                    ),
                 ],
                 align = 'center',
                 no_gutters = True,
            ),
        ),
    ],
    brand = '   ',
    brand_href = '/',
    expand = 'lg',
    color="primary",
    id='navBar',
    light = False,
    dark = True,
)

def get():
    return navbar
