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
    '''
    ),

    html.Img(src=app.get_asset_url('images/Main_Help_Data.png'), style = dict(width = 400)),

    dcc.Markdown('''
**Select** the data columns you want to plot using the dropdowns.
To create the z-axis, set the scatter to 3D in the top right of the page and select the z-axis variable.

**Slide** between sheets, or data files, with the slide feature at the bottom of the page.

**Click** on data points when in 2D mode to see the values of the variables you
plotted. Note: the points are *not* clickable in 3D mode.

**Filter** the data to plot using the Filter Data button.
The plot contains selected data or all rows if none are selected.
Filter arguments can be simple searches or inequalities (eg. < 60).
Download the plotted data in the navigation bar.

### Categorical Data
Wiz automatically parses whether your data is categorical. Categorical includes any data with text or a list of integers with less than 20 unique values.

## Plot Types
If only one variable is plotted (x), a histogram is plotted.

If two variables are selected (x and y) and the x variable is categorical,
box plots are plotted.

Otherwise, all plots are scatter-type.

'''
    )
]


modal = html.Div(
    dbc.Modal(
    [
        dbc.ModalHeader(
            dbc.Button("Close", id="main-help-close", className="ml-auto")
        ),
        dbc.ModalBody(help_content),
    ],
    id="main-help-modal",
    size = 'lg',
    scrollable = True,
    ),
)


def get():
    return modal
