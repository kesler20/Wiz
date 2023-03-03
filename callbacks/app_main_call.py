##==================================
## External imports
##==================================
import urllib
import time
import datetime
import dash
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

##==================================
## Internal imports
##==================================
from app import app
from functions.global_functions import *
from functions.app_main.data import *
from functions.app_main.graph import *
from layouts.app_main_layout import graph

##==================================
## Callbacks
##==================================
# Upload data and create data slider
@app.callback(
    [
        Output('main-slider','marks'),
        Output('main-slider','min'),
        Output('main-slider','max'),
        Output('main-slider','value'),
        Output('main-loading-upload', 'children'),
        Output('main-session-id','children'),
    ],
    [
        Input('main-file-upload','contents'),
        Input('main-file-upload','filename'),
    ],
    [
        State('main-session-id','children'),
    ],
    prevent_initial_call = True,
)
def process_data_upload(file_contents, file_name, session_id):
    # Don't update if there is no data
    if file_contents is None:
        raise PreventUpdate

    # Get a new session ID for the new file
    session_id = genSession()

    # Get the uploaded data
    all_data = get_data(session_id, file_contents, file_name)

    # Populate the slider bar with the sheet options
    sheets = list(all_data)
    slider_out = {i : sheets[i] for i in range(len(sheets))}
    slider_min = 0
    slider_max = len(sheets) - 1

    # Delete oldest cache if it is accumulating
    path = os.getcwd() + '/' + CACHE_DIRECTORY + '/'
    delete_cache(path)

    out = dcc.Upload(
        html.H6(
        'Clear previous data to upload again'),
        style_active  = dict(
            borderStyle     = 'solid',
            borderColor     = '#0FA0CE',
            backgroundColor = '#eee',
        ),
        multiple      = True,
        loading_state = dict(
            is_loading = False,
        ),
        id            = 'main-file-upload',
        className     = 'upload',
        disabled      = True,
        contents      = None
    )

    return slider_out, slider_min, slider_max, slider_min, out, session_id

# Populate dropdowns
@app.callback(
    [
        Output('main-x-select','options'),
        Output('main-y-select','options'),
        Output('main-z-select','options'),
        Output('main-c-select','options'),
        Output('main-s-select','options'),
        Output('main-x-select','value'),
        Output('main-y-select','value'),
        Output('main-z-select','value'),
        Output('main-c-select','value'),
        Output('main-s-select','value'),
    ],
    [
        Input('main-slider','value'),
    ],
    [
        State('main-session-id','children'),
        State('main-file-upload','contents'),
        State('main-file-upload','filename'),
        State('main-x-select','value'),
        State('main-y-select','value'),
        State('main-z-select','value'),
        State('main-c-select','value'),
        State('main-s-select','value')
    ],
    prevent_initial_call = True,
)
def populate_dropdowns(sheet_num, session_id, file_contents, file_name, x_value, y_value, z_value, c_value, s_value):
    # Don't update if there is no session ID
    if session_id is None:
        raise PreventUpdate

    # Load data
    data = get_data(session_id, file_contents, file_name)

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

    # Keep the current value if is present in new set of options
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

    return x, y, z, c, s, x_out, y_out, z_out, c_out, s_out

# Turn z-axis selector on or off
@app.callback(
    Output('main-z-select','disabled'),
    [
        Input('main-graph-type', 'value'),
    ],
    prevent_initial_call = True
)
def activate_z(graph_type):
    if graph_type == 2:
        z_disabled = False
    else:
        z_disabled = True
    return z_disabled

# Callback to update graph
@app.callback(
    [
        Output('main-graph','figure'),
        Output('main-graph','style'),
        Output('main-graph','animate'),
        Output('main-graph','config'),
        Output('main-graph','className'),
        Output('main-display-size-scale','style'),
        Output('main-min-size','children'),
        Output('main-max-size','children'),
        Output('main-graph-timestamp','children'),
        Output('main-table-filter','children'),
        Output('main-table-selected-rows','children'),
    ],
    [
        Input('main-x-axis-type','value'),
        Input('main-y-axis-type','value'),
        Input('main-graph-type','value'),
        Input('main-graph','clickData'),
        Input('main-x-select','value'),
        Input('main-y-select','value'),
        Input('main-c-select','value'),
        Input('main-s-select','value'),
        Input('main-z-select','value'),
        Input('main-z-select','disabled'),
        Input('main-data-table','filter_query'),
        Input('main-data-table','selected_rows'),
    ],
    [
        State('main-data-table','sort_by'),
        State('main-graph-timestamp','children'),
        State('main-slider','value'),
        State('main-session-id','children'),
        State('main-file-upload','contents'),
        State('main-file-upload','filename'),
        State('main-table-filter','children'),
        State('main-table-selected-rows','children'),
    ],
    prevent_initial_call = True
)
def update_graph(x_type, y_type, graph_type, click_data, x_column,
    y_column, c_column, s_column, z_column, z_off,
    filter_query, selected_rows, sort_by,
    graph_timestamp, sheet_num, session_id, file_contents, file_name,
    prev_filter_query, prev_selected_rows):
    # Set the current time for output
    date_out = datetime.datetime.now()

    # Get info on what triggered the callback
    ctx = dash.callback_context

    # Do any necessary processing on the callback triggers
    if not ctx.triggered:
        trigger_id = None
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        prop_id = ctx.triggered[0]['prop_id'].split('.')[1]

        # Don't update if the selected rows did not change didn't change
        if filter_query is None:
            filter_query = ''
        if prev_filter_query is None:
            prev_filter_query = ''
        if selected_rows is None:
            selected_rows = []
        if prev_selected_rows is None:
            prev_selected_rows = []
        if 'filter_query' in prop_id and selected_rows != []:
            selected_rows = []
            prev_selected_rows = []
            raise PreventUpdate
        if 'filter_query' in prop_id and filter_query in prev_filter_query:
            if not filter_query and not prev_filter_query:
                raise PreventUpdate
        if 'selected_rows' in prop_id and selected_rows is prev_selected_rows:
            raise PreventUpdate

        # If the click data does not trigger, that means the graph is changing (get rid of click data)
        #    If click data is the only thing updated, then don't update the timestamp
        if 'main-graph' not in trigger_id:
            click_data = None
        else:
            date_out = graph_timestamp

        # Don't update the timestamp if only filtering or row-select is occuring
        if 'main-data-table' in trigger_id:
            date_out = graph_timestamp

    # Return default values if there is no data uploaded
    if session_id is None:
        return dict(data = [], layout = blank_layout()), dict(height = '100%', width = '100%'), False, graph_configure(False), dict(display = 'none'), None, None, date_out, None, None

    # Don't update if the z-axis is available without an input
    if (z_column is None or z_column == []) and not z_off:
        raise PreventUpdate

    # Load in all data from cache
    data = get_data(session_id, file_contents, file_name)

    # Get the name of the sheet
    sheet = list(data)[sheet_num]

    # Get data from the specified sheet
    sub_data = data[sheet]

    # Reduce the only what is needed to plot
    plot_data = get_plot_data(sub_data, x_column, y_column, c_column, s_column, z_column, z_off)
    columns = list(plot_data)

    # Pickle the plot data for other processes to use
    pickleData(plot_data,session_id)

    # Filter the data based on filtering in the data table
    plot_data = filter_data(plot_data, filter_query, sort_by, selected_rows)

    # Determine figure type from data
    out_style, out_figure, animate = pick_plot(plot_data, columns, click_data, x_type, y_type, graph_type)

    # Configuration for figure (Need to have two columns for plot)
    if columns is not None and columns != []:
        if len(columns) > 1:
            configure_graph = graph_configure('hover')
        else:
            configure_graph = graph_configure(False)
    else:
        configure_graph = graph_configure(False)

    # Size axis labels
    if columns is not None and columns != []:
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
    else:
        min_size = None
        max_size = None
        display_style = dict(display = 'none')

    # Change the class name if the plot is 3D (only necessary if the theme is changed)
    if graph_type == 2:
        className = 'threeDgraph'
        out_style = dict(height = '100%', width = '99.999%')
    else:
        className = ''
        out_style = dict(height = '100%', width = '100%')

    return out_figure, out_style, animate, configure_graph, className, display_style, min_size, max_size, date_out, filter_query, selected_rows

# Update data table
@app.callback(
    [
        Output('main-table-container','children'),
        Output('main-table-timestamp','children'),
    ],
    [
        Input('main-table-open', 'n_clicks'),
        Input('main-data-table','page_current'),
        Input('main-data-table','sort_by'),
        Input('main-data-table','filter_query'),
    ],
    [
        State('main-data-table','selected_rows'),
        State('main-table-timestamp','children'),
        State('main-graph-timestamp','children'),
        State('main-session-id','children'),
        State('main-x-select','value')
    ],
    prevent_initial_call = True,
)
def update_table(n_clicks_open, page_current, sort_by, filter_query, selected_rows, table_timestamp, graph_timestamp, session_id, x_column):
    # Set the current time for output
    date_out = datetime.datetime.now()

    # Don't update if there is no data
    if session_id is None or x_column is None or x_column == []:
        return empty_table('main-data-table'), table_timestamp

    # Get info on what triggered the callback
    ctx = dash.callback_context

    # Do any necessary processing on the callback triggers
    if not ctx.triggered:
        trigger_id = None
    else:
        trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]
        prop_id    = ctx.triggered[0]['prop_id'].split('.')[1]

        # Controls for when the "open" button opened the table
        if 'main-table-open' in trigger_id:
            # Don't update the table if the graph hasn't updated
            if table_timestamp is not None:
                if graph_timestamp is None:
                    raise PreventUpdate
                if table_timestamp > graph_timestamp:
                    raise PreventUpdate

        # Controls for when a table property was changed
        if 'page_current' in prop_id:
            date_out = table_timestamp
        if 'sort_by' in prop_id:
            date_out = table_timestamp
        if 'filter_query' in prop_id:
            selected_rows = []
            date_out = table_timestamp


    # Get the plotted data from unpickling it
    plot_data = unpickleData(session_id)


    # Process inputs that may not be set
    if selected_rows is None:
        selected_rows = []
    if filter_query is None:
        filter_query = ''
    if sort_by is None:
        sort_by = []
    if page_current is None:
        page_current = 0

    # Get the data to display and properties of the table
    table_data, page_size, page_count, columns = backend_table(plot_data, filter_query, sort_by, page_current)

    # Get table styling
    css, style_table, style_cell = data_table_style()

    # Build output table
    table = dt.DataTable(
        id             = 'main-data-table',
        data           = table_data,
        columns        = columns,

        page_action    = 'custom',
        page_current   = page_current,
        page_size      = page_size,
        page_count     = page_count,

        row_selectable = "multi",
        selected_rows  = selected_rows,

        sort_action    = 'custom',
        sort_mode      = 'single',
        sort_by        = sort_by,
        filter_action  = 'custom',
        filter_query   = filter_query,

        editable       = False,
        row_deletable  = False,

        css            = css,
        style_table    = style_table,
        style_cell     = style_cell,
    )

    return table, date_out

# Update download link for plotted data
@app.callback(
    Output('main-download-link','href'),
    [
        Input('main-session-id','children')
    ],
    prevent_initial_call = True
)
def update_download_link(sessionID):
    return '/' + CACHE_DIRECTORY + '?value={}'.format(sessionID)


# Help modal
@app.callback(
    Output('main-help-modal', 'is_open'),
    [
        Input('main-help-close', 'n_clicks'),
        Input('main-help-open', 'n_clicks'),
    ],
    [
        State('main-help-modal','is_open')
    ],
    prevent_initial_call = True,
)
def help_modal(n_clicks_close, n_clicks_open, is_open):
    if n_clicks_open or n_clicks_close:
        return not is_open
    return is_open

# Data table modal (closes modal on initial callback - tricky but necessary!)
@app.callback(
    Output('main-table-modal', 'is_open'),
    [
        Input('main-table-close', 'n_clicks'),
        Input('main-table-open', 'n_clicks'),
    ],
    [
        State('main-table-modal','is_open')
    ],
)
def table_modal(n_clicks_close, n_clicks_open, is_open):
    return not is_open
