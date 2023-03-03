import os
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo, data_table
from layouts.examples.example_4_layout import app_navbar, top_row, size_scale, graph, axis_select

import pandas as pd
from functions.example_4.data import *
from functions.example_4.graph import *

# Load in dataset as global variable
import static_datasets.datasets as glob_data

##==================================
## Dataset
##==================================
all_data = glob_data.example_4

##==================================
## Initial data that is plotted
##==================================
# Columns
column_num = [0, 1, 2];

# Get the name of the sheet
sheet = list(all_data)[0]

# Get data from the specified sheet
sub_data = all_data[sheet]

# Get the column names of the plotted area
columns = []
for i in column_num:
    columns.append(list(sub_data)[i])

plot_data = sub_data[columns]

# Initialze graph
out_style, out_figure, animate = pick_plot(plot_data, columns, None, 'linear', 'linear', 1)

# Configuration for figure
configure_graph = graph_configure()

##==================================
## Slider
##==================================
# Populate the slider bar with the sheet options
sheets = list(all_data)

slider_marks = {i : sheets[i] for i in range(len(sheets))}
slider_min = 0
slider_max = len(sheets) - 1

slider = dbc.Col(
    [
        html.Div(
            [
                dcc.Slider(
                    id = 'example-4-slider',
                    min = slider_min,
                    max = slider_max,
                    marks = slider_marks,
                    value = 0,
                    updatemode = 'mouseup'
                    )
            ],
            id = 'example-4-slider-call',
            className = 'slider'
        )
    ],
    width = dict(size = 6, offset = 3),
    id = 'example-4-filter-slider'
)

##==================================
## Dropdowns
##==================================
# Get labels
labels, size_labels = get_labels(sub_data)

# Set options
options = [{'label': i, 'value': i} for i in labels]
size_options = [{'label': i, 'value': i} for i in size_labels]
initial_values = [columns[1], columns[2], None, None, None]

##==================================
## Assemble layout
##==================================
out = [
    app_navbar.get(),
    top_row.get(),
    size_scale.get(),
    graph.get(out_style, out_figure, configure_graph),
    axis_select.get(options, size_options, initial_values),
    slider,
    data_table.get_table('example-4-data-table-plot'),
    html.Div([],id='example-4-lastplot', style=dict(display = 'none')),
    html.Div(genSession(),id='example-4-session-id', style=dict(display='none')),
]

def layout():
    return out
