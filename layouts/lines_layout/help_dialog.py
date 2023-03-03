import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import app

help_content = [
    dcc.Markdown('''
## Usage


**Upload** data in the top left-hand side of the app. One spreadsheet (Excel or OpenDocument) or multiple CSVs/DATs/TXTs are accepted. Data is read in assuming the
first column has data labels and the top row has column labels (see below).

There are two ways to input data...
#### Type 1
'''
    ),

    html.Img(src=app.get_asset_url('images/Lines_Help_Data_1.png'), style = dict(width = 400)),

    dcc.Markdown('''
#### Type 2
'''
    ),

    html.Img(src=app.get_asset_url('images/Lines_Help_Data_2.png'), style = dict(width = 400)),

    dcc.Markdown('''
**Select** the series that you want to plot using the dropdown. Multiple can be selected.

**Slide** between sheets, or data files, with the slide feature at the bottom of the page.

**Filter** the data to plot using the Filter Data button.
The plot contains selected data or all rows if none are selected.
Filter arguments can be simple searches or inequalities (eg. < 60).
Download the plotted data in the navigation bar.

### Categorical Data
Wiz automatically parses whether your data is categorical. Categorical includes any data with text or a list of integers with less than 20 unique values.
'''
    )
]


modal = html.Div(
    dbc.Modal(
    [
        dbc.ModalHeader(
            dbc.Button("Close", id="lines-help-close", className="ml-auto")
        ),
        dbc.ModalBody(help_content),
    ],
    id="lines-help-modal",
    size = 'lg',
    scrollable = True,
    ),
)


def get():
    return modal
