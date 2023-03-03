import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Axes selectors
##==================================
def get(options, initial_value):
    out = dbc.Col([
            dbc.Row([
                    # Y-Axis Dropdown Selector
                    html.Div([
                        dcc.Dropdown(
                            id='example-3-y-select',
                            options = options,
                            placeholder = 'Select...',
                            clearable = False,
                            multi = True,
                            value = initial_value,
                        )
                    ], className = 'dropdown-axis', style = dict(width = 400)
                    ),
            ], justify = 'center', align = 'center'),
            dbc.Row([
                html.Div([
                    html.P('y: ')
                ], className = 'dropdown-label'
                ),


                html.Div([
                    dbc.RadioItems(
                        id = 'example-3-y-axis-type',
                        options = [
                            dict(label = 'Linear' , value = 'linear'),
                            dict(label = 'Log', value = 'log')
                        ],
                        value = 'linear',
                        inline=True,
                    )
                ], className = 'axis-type'
                )

            ], justify = 'center'),
        ],
        id = 'example-3-axis-dropdowns',
        width = dict(size = 12, offset = 0),
        style = dict(
            marginTop = 30,
            marginLeft = 0,
            marginRight = 0,
        ),
        align = 'center',
    )

    return out
