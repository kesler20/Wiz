##==================================
## External imports
##==================================
import urllib
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

##==================================
## Internal imports
##==================================
from app import app
from functions.example_2.data import *
from functions.example_2.graph import *
import static_datasets.datasets as glob_data

##==================================
## Callbacks
##==================================
# Populate dropdowns
@app.callback(
    [
        Output('example-2-x-select','options'),
        Output('example-2-y-select','options'),
        Output('example-2-z-select','options'),
        Output('example-2-c-select','options'),
        Output('example-2-s-select','options'),
        Output('example-2-x-select','value'),
        Output('example-2-y-select','value'),
        Output('example-2-z-select','value'),
        Output('example-2-c-select','value'),
        Output('example-2-s-select','value'),
        Output('example-2-main-graph','clickData'),
    ],
    [
        Input('example-2-slider','value'),
    ],
    [
        State('example-2-x-select','value'),
        State('example-2-y-select','value'),
        State('example-2-z-select','value'),
        State('example-2-c-select','value'),
        State('example-2-s-select','value')
    ]
)
def populate_dropdowns(sheet_num, x_value, y_value, z_value, c_value, s_value):
    # Get data
    data = glob_data.example_2

    # Get the name of the sheet
    sheet = list(data)[sheet_num]

    # Get data from the specified sheet
    sub_data = data[sheet]

    # Get labels
    labels, size_labels = get_labels(sub_data)

    # Set options
    options = [{'label': i, 'value': i} for i in labels]
    size_options = [{'label': i, 'value': i} for i in size_labels]

    x = options;
    y = options;
    z = options;
    c = options;
    s = size_options;

    if x_value in [item['label'] for item in options]:
        x_out = x_value
    else:
        x_out = None

    if y_value in [item['label'] for item in options]:
        y_out = y_value
    else:
        y_out = None

    if z_value in [item['label'] for item in options]:
        z_out = z_value
    else:
        z_out = None

    if c_value in [item['label'] for item in options]:
        c_out = c_value
    else:
        c_out = None

    if s_value in [item['label'] for item in size_options]:
        s_out = s_value
    else:
        s_out = None

    return x, y, z, c, s, x_out, y_out, z_out, c_out, s_out, None

# Turn z-axis selector on or off
@app.callback(
    Output('example-2-z-select','disabled'),
    [
        Input('example-2-graph-type', 'value'),
    ]
)
def activate_z(graph_type):
    if graph_type == 2:
        z_disabled = False
    else:
        z_disabled = True
    return z_disabled

# Handle graph data
@app.callback(
    [
        Output('example-2-main-graph','figure'),
        Output('example-2-main-graph','animate'),
        Output('example-2-main-graph','style'),
        Output('example-2-main-graph','className'),
        Output('example-2-display-size-scale','style'),
        Output('example-2-min-size','children'),
        Output('example-2-max-size','children'),
        Output('example-2-lastplot','children'),
    ],
    [
        Input('example-2-x-select','value'),
        Input('example-2-y-select','value'),
        Input('example-2-c-select','value'),
        Input('example-2-s-select','value'),
        Input('example-2-z-select','value'),
        Input('example-2-z-select','disabled'),
        Input('example-2-x-axis-type','value'),
        Input('example-2-y-axis-type','value'),
        Input('example-2-graph-type','value'),
        Input('example-2-main-graph','clickData'),
    ],
    [
        State('example-2-slider','value'),
        State('example-2-lastplot','children'),
        State('example-2-session-id','children')
    ],
    prevent_initial_call = True,
)
def update_graph(x_column, y_column, c_column, s_column, z_column, z_off,x_type, y_type, graph_type, click_data, sheet_num, last_plot,session_id):
    # Get data
    data = glob_data.example_2

    # Get info on what triggered the callback
    ctx = dash.callback_context

    # Do any necessary processing on the callback triggers
    if not ctx.triggered:
        trigger_id = None
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        prop_id = ctx.triggered[0]['prop_id'].split('.')[1]
        # If the click data does not trigger, that means the graph is changing (get rid of click data)
        if 'main-graph' not in trigger_id:
            click_data = None

    # Don't update if the z-axis is available without an input
    if (z_column is None or z_column == []) and not z_off:
        z_column = None
        graph_type = 1
        z_off = True

    # Get the maximum data to set the layout
    if z_column is not None:
        x_range, y_range, z_range = get_ranges(data, x_type, y_type, x_column, y_column, z_column)
    else:
        x_range, y_range, z_range = get_ranges(data, x_type, y_type, x_column, y_column, x_column)

    # Get the name of the sheet
    sheet = list(data)[sheet_num]

    # Get data from the specified sheet
    sub_data = data[sheet]

    # Get column names
    columns = [sub_data.columns[0], x_column, y_column, c_column, s_column, z_column]

    # Clean data
    plot_data = clean_data_static(sub_data, x_column, y_column, c_column,s_column, z_column, z_off)

    # Store the plot data for downloading
    pickleData(plot_data,session_id)

    # Get plotly figure object
    out_figure = update_plot(plot_data, click_data, x_type, y_type, graph_type, x_range, y_range, z_range)

    # Configuration for figure
    configure_graph = graph_configure()

    # Size axis labels
    if len(columns) > 4:
        # Get min and max size
        size_range = [plot_data.iloc[:,4].min(), plot_data.iloc[:,4].max()]
        size_axis = format_size([plot_data.iloc[:,4].min(), plot_data.iloc[:,4].max()])
        min_size = size_axis[0]
        max_size = size_axis[1]
        display_style = dict(display = 'block')
    else:
        min_size = None
        max_size = None
        display_style = dict(display = 'none')

    # Store previous plot type
    new_plot = graph_type

    # To animate or not?
    if new_plot == last_plot:
        animate = True
    else:
        animate = False

    # Override to fix crashing issue
    animate = False

    # Change the class name if the plot is 3D  (only necessary if the theme is changed)
    if graph_type == 2:
        className = 'threeDgraph'
        out_style = dict(height = '100%', width = '99.999%')
    else:
        className = ''
        out_style = dict(height = '100%', width = '100%')

    return out_figure, animate, out_style, className, display_style, min_size, max_size, new_plot

# Update download link for plotted data
@app.callback(
    Output('example-2-download-link', 'href'),
    [
        Input('example-2-session-id','children')
    ]
)
def update_download_link(sessionID):
    return '/' + CACHE_DIRECTORY + '?value={}'.format(sessionID)
