##==================================
## External imports
##==================================
import urllib
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

##==================================
## Internal imports
##==================================
from app import app
from functions.example_5.data import *
from functions.example_5.graph import *
import static_datasets.datasets as glob_data

##==================================
## Callbacks
##==================================
# Populate dropdowns
@app.callback(
    [
        Output('example-5-class-select','options'),
        Output('example-5-class-select','value'),
    ],
    [
        Input('example-5-slider','value'),
        Input('example-5-analysis-type','value')
    ],
    [
        State('example-5-class-select','value'),
    ]
)
def populate_dropdowns(sheet_num, analysis_type, class_value):
    # Get data
    data = glob_data.example_5

    # Get the name of the sheet
    sheet = list(data)[sheet_num]

    # Get data from the specified sheet
    sub_data = data[sheet]

    # Get labels
    class_labels = get_labels(sub_data)

    # Set options
    options = [{'label': i, 'value': i} for i in class_labels]
    classes = options;

    # If the new options have the previous value, then set it
    if class_value in [item['label'] for item in options]:
        class_out = class_value;
    else:
        class_out = None


    # LDA requires classes
    if class_out is None and analysis_type == 2:
        class_out = classes[0]['value']

    return classes, class_out

# Handle graph data and fill in table
@app.callback(
    [
        Output('example-5-graph','figure'),
        Output('example-5-graph','style'),
        Output('example-5-graph','config'),
        Output('example-5-graph-2','figure'),
        Output('example-5-graph-2','style'),
        Output('example-5-graph-2','config'),
        Output('example-5-download-link', 'href')
    ],
    [
        Input('example-5-analysis-type','value'),
        Input('example-5-graph','clickData'),
        Input('example-5-class-select','value'),
        Input('example-5-slider','value'),
    ],
    [
        State('example-5-session-id','children')
    ],
    prevent_initial_call = True
)
def update_PCA_graph(analysis_type, click_data, class_select, sheet_num,session_id):
    # Get data
    data = glob_data.example_5

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

    # Get the name of the sheet
    sheet = list(data)[sheet_num]

    # Get data from the specified sheet
    plot_data = data[sheet]

    # Do analysis and plot based on the input type
    if analysis_type == 1:
        # Analysis
        Y, var_exp, cum_var_exp = PCA(plot_data, class_select)
        type = 'PC'

        # Get figuress
        out_style, out_figure, animate = PCA_plot(Y, plot_data, var_exp, cum_var_exp, class_select, click_data)
        out_style_2, out_figure_2 = PCA_plot_2(var_exp, cum_var_exp)

    else:
        # Analysis
        Y_lda, var_exp, cum_var_exp = LDA(plot_data, class_select)
        type = 'LD'

        # Determine figure type from data
        out_style, out_figure, animate = LDA_plot(Y_lda, plot_data, var_exp, cum_var_exp, class_select)
        out_style_2, out_figure_2 = LDA_plot_2(var_exp, cum_var_exp)

    # Configuration for figure
    if len(list(plot_data)) < 1:
        value = False
    else:
        value = 'hover'

    configure_graph = graph_configure(value)


    # Make download link data
    n = len(var_exp)
    df = pd.DataFrame(Y, columns = [type + ' %s' %i for i in range(1, n+1)]);
    temp = np.array([var_exp, cum_var_exp])
    df1 = pd.DataFrame({'Individual': var_exp, 'Cumulative': cum_var_exp})
    dff = pd.concat([df,df1], axis=1)
    pickleData(dff, session_id + 'analysis')
    link_ref = '/' + CACHE_DIRECTORY + '?value={}'.format(session_id + 'analysis')

    return out_figure, out_style, configure_graph, out_figure_2, out_style_2, configure_graph, link_ref
