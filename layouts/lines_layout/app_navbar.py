import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Navigation bar
##==================================
download_link = html.A(
    'Download Plot Data',
    id = 'lines-download-link',
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
                    dbc.NavItem(dbc.NavLink(download_link),id='lines-dowload-nav'),
                    dbc.NavItem(dbc.NavLink('Data Table',id='lines-table-open'), style = dict(cursor = 'pointer')),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem('Scatter', href="/"),
                        ],
                        label = "Plot Types",
                        nav = True,
                        id = 'lines-plot-types'
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem('PCA/LDA', href="/pca"),
                        ],
                        label = "Analysis",
                        nav = True,
                        id = 'lines-analysis-types'
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem('Page Help', id='lines-help-open'),
                            dbc.DropdownMenuItem('Documentation', href='/help'),
                            dbc.DropdownMenuItem('Examples', href='/examples'),
                            dbc.DropdownMenuItem('Contact Us', href='/contact-us'),
                        ],
                        label = "Help",
                        nav = True,
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
