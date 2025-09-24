from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

##==================================
## Graph type selector
##==================================
# Label
radio_label = html.H6('Scatter Type:', style = dict(marginRight = 7))

# Radio buttons
radios = dbc.FormGroup(
    [
        dbc.RadioItems(
            id = 'example-1-graph-type',
            options=[
                {"label": "2D", "value": 1},
                {"label": "3D", "value": 2},
            ],
            value=1,
            inline=True,
        ),
    ]
)


radio_select = dbc.Col(
    [
        dbc.Row(
            [
                radio_label,
                radios
            ],
            justify = 'center'
        )
    ],
    id = 'example-1-radio-container', width = 4, align = 'end'
)


##==================================
## Assemble layout
##==================================
output = dbc.Row(
    [
        radio_select
    ],
    justify = 'end',
    style = dict(marginTop = 5, marginBottom = 10)
)



def get():
    return output
