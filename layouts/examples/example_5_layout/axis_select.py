from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

##==================================
## Selectors
##==================================
def get(class_options):
    out = dbc.Col([
            dbc.Row([
                # Class selector (what differentiates the data)
                dbc.Col([
                    html.Div([
                        html.P('Classes:    ')
                    ], className = 'dropdown-label', style = dict(marginRight = 30)
                    ),

                    html.Div([
                        dcc.Dropdown(
                            id='example-5-class-select',
                            options = class_options,
                            placeholder = 'Select...',
                            clearable = True,
                        )
                    ], className = 'dropdown-axis'
                    ),

                ], className = 'dropdown-group'
                ),
            ], justify = 'center'),
        ],
        id = 'example-5-axis-dropdowns',
        width = dict(size = 12, offset = 0),
        style = dict(
            marginTop = 30,
            marginLeft = 0,
            marginRight = 0,
        ),
        align = 'center',
    )


    return out
