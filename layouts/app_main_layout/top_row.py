import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

##==================================
## Upload component
##==================================
upload = dbc.Col([
    dcc.Loading(
        dcc.Upload(
            html.H6([
                'Drag and Drop or ',
                html.A('Select a File')
            ]),
            style_active = dict(
                borderStyle = 'solid',
                borderColor = '#0FA0CE',
                backgroundColor = '#eee',
                ),
            multiple = True,
            loading_state = dict(
                is_loading = False,
            ),
            id = 'main-file-upload',
            className = 'upload',
        ),
        id="main-loading-upload",
        fullscreen=False,
    ),
    ],
    id = 'main-upload',
    width = dict(size = 3, offset = 1),
    style = dict(zIndex = 1001),
    align = 'center'
)

##==================================
## Graph type selector
##==================================
# Label
radio_label = html.H6('Scatter Type:', style = dict(marginRight = 7))

# Radio buttons
radios = dbc.FormGroup(
    [
        dbc.RadioItems(
            id = 'main-graph-type',
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
    id = 'main-radio-container', width = 4, align = 'end'
)


##==================================
## Assemble layout
##==================================
output = dbc.Row(
    [
        upload,
        radio_select
    ],
    justify = 'between',
    align = 'center',
    style = dict(marginTop = 5, marginBottom = 10)
)



def get():
    return output
