from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

##==================================
## Slider
##==================================
out = dbc.Col(
    [
        html.Div(
            [
                dcc.Slider(
                    id = 'main-slider',
                    min = 0,
                    max = 0,
                    marks = {},
                    value = 0,
                    updatemode = 'drag'
                    )
            ],
            id = 'main-slider-call',
            className = 'slider'
        )
    ],
    width = dict(size = 6, offset = 3),
    id = 'main-filter-slider'
)

def get():
    return out
