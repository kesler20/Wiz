import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Axes selectors
##==================================
out = dbc.Col([
    dbc.Row([
            # X-Axis Dropdown Selector
            dbc.Col([
                html.Div([
                    html.P('x: ')
                ], className = 'dropdown-label'
                ),

                html.Div([
                    dcc.Dropdown(
                        id='main-x-select',
                        options = [],
                        placeholder = 'Select...',
                        clearable = False,
                    )
                ], className = 'dropdown-axis'
                ),

                html.Div([
                    dbc.RadioItems(
                        id = 'main-x-axis-type',
                        options = [
                            dict(label = 'Linear' , value = 'linear'),
                            dict(label = 'Log', value = 'log')
                        ],
                        value = 'linear',
                        inline=True,
                    )
                ], className = 'axis-type'
                )
            ], className = 'dropdown-group'
            ),

            # Y-Axis Dropdown Selector
            dbc.Col([
                html.Div([
                    html.P('y: ')
                ], className = 'dropdown-label'
                ),

                html.Div([
                    dcc.Dropdown(
                        id='main-y-select',
                        options = [],
                        placeholder = 'Select...',
                        clearable = True,
                    )
                ], className = 'dropdown-axis'
                ),

                html.Div([
                    dbc.RadioItems(
                        id = 'main-y-axis-type',
                        options = [
                            dict(label = 'Linear' , value = 'linear'),
                            dict(label = 'Log', value = 'log')
                        ],
                        value = 'linear',
                        inline=True,
                    )
                ], className = 'axis-type'
                )
            ], className = 'dropdown-group'
            ),

            # Color Axis Dropdown Selector
            dbc.Col([
                html.Div([
                    html.P('color: ')
                ], className = 'dropdown-label'
                ),

                html.Div([
                    dcc.Dropdown(
                        id='main-c-select',
                        options = [],
                        placeholder = 'Select...',
                        clearable = True,
                    )
                ], className = 'dropdown-axis'
                ),

            ], className = 'dropdown-group'
            ),

            # Size Axis Dropdown Selector
            dbc.Col([
                html.Div([
                    html.P('size: ')
                ], className = 'dropdown-label'
                ),

                html.Div([
                    dcc.Dropdown(
                        id='main-s-select',
                        options = [],
                        placeholder = 'Select...',
                        clearable = True,
                    )
                ], className = 'dropdown-axis'
                ),

            ], className = 'dropdown-group'
            ),



            # Z-Axis Dropdown Selector
            dbc.Col([
                html.Div([
                    html.P('z: ')
                ], className = 'dropdown-label'
                ),

                html.Div([
                    dcc.Dropdown(
                        id='main-z-select',
                        options = [],
                        placeholder = 'Select...',
                        clearable = True,
                        disabled = True
                    )
                ], className = 'dropdown-axis'
                ),

            ], className = 'dropdown-group'
            )
        ])
    ],
    id = 'main-axis-dropdowns',
    width = dict(size = 12, offset = 0),
    style = dict(
        marginTop = 30,
        marginLeft = 0,
        marginRight = 0,
    ),
    align = 'center'
)

def get():
    return out
