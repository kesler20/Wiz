##==================================
## External imports
##==================================
import urllib
import dash
import datetime as dt
import pandas_datareader.data as webDR
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

##==================================
## Internal imports
##==================================
from app import app
from functions.example_3.data import *
from functions.example_3.graph import *
import static_datasets.datasets as glob_data

##==================================
## Callbacks
##==================================
# Handle graph data and fill in table
@app.callback(
    [
        Output('example-3-graph','figure'),
        Output('example-3-graph','style'),
        Output('example-3-graph','animate'),
        Output('example-3-graph','config'),
    ],
    [
        Input('example-3-y-select','value'),
        Input('example-3-slider','value'),
        Input('example-3-y-axis-type','value'),
    ],
    [
        State('example-3-session-id','children')
    ]
)
def update_graph(y_columns, slider_value, y_type,session_id):
    # Get data
    df = glob_data.example_3

    # Filter data based on range selected
    df = df[(df['Date'] > str(slider_value[0]) + '-01-01') & (df['Date'] < str(slider_value[1]+1) + '-01-01')]

    # Column indicies
    cols = []
    cols.append(0)
    for n in y_columns:
        cols.append(df.columns.get_loc(n))

    # Reduce data to what needs to be plotted or displayed in the table
    if y_columns is not None:
        plot_data = df[df.columns[cols]]

    else:
        plot_data = df[[df.columns[0]]]

    # Store the plot data for downloading
    pickleData(plot_data,session_id)

    # Determine figure type from data
    datatype = 1
    out_style, out_figure, animate = update_plot(plot_data, y_columns, None, 'linear', y_type, datatype)

    # Configuration for figure
    configure_graph = graph_configure()

    return out_figure, out_style, animate, configure_graph

# Update download link for plotted data
@app.callback(
    Output('example-3-download-link', 'href'),
    [
        Input('example-3-session-id','children')
    ]
)
def update_download_link(sessionID):
    return '/' + CACHE_DIRECTORY + '?value={}'.format(sessionID)
