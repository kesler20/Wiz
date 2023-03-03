import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Axes selectors
##==================================
def get(options, size_options,initial_value):
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
                            id='example-4-x-select',
                            options = options,
                            value = initial_value[0],
                            placeholder = 'Select...',
                            clearable = False,
                        )
                    ], className = 'dropdown-axis'
                    ),

                    html.Div([
                        dbc.RadioItems(
                            id = 'example-4-x-axis-type',
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
                            id='example-4-y-select',
                            options = options,
                            value = initial_value[1],
                            placeholder = 'Select...',
                            clearable = True,
                        )
                    ], className = 'dropdown-axis'
                    ),

                    html.Div([
                        dbc.RadioItems(
                            id = 'example-4-y-axis-type',
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
                            id='example-4-c-select',
                            options = options,
                            value = initial_value[2],
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
                            id='example-4-s-select',
                            options = size_options,
                            value = initial_value[3],
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
                            id='example-4-z-select',
                            options = options,
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
        id = 'example-4-axis-dropdowns',
        width = dict(size = 12, offset = 0),
        style = dict(
            marginTop = 30,
            marginLeft = 0,
            marginRight = 0,
        ),
        align = 'center'
    )

    return out
