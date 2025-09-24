from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

##==================================
## Graph type selector
##==================================
# Label
radio_label = html.H6('Analysis:', style = dict(marginRight = 7))

# Radio buttons
radios = dbc.FormGroup(
    [
        dbc.RadioItems(
            id = 'example-5-analysis-type',
            options=[
                {"label": "PCA", "value": 1},
                {"label": "LDA", "value": 2},
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
    id = 'example-5-radio-container', width = 4, align = 'end'
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
