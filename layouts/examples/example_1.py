import os
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from layouts.global_layout import bubble_nav_logo, data_table
from layouts.examples.example_1_layout import app_navbar, top_row, size_scale, graph, axis_select

import pandas as pd
from functions.example_1.data import *
from functions.example_1.graph import *

# Load in dataset as global variable
import static_datasets.datasets as glob_data

##==================================
## Dataset
##==================================
all_data = glob_data.example_1

##==================================
## Initial data that is plotted
##==================================
# Columns
column_num = [0, 1, 2, 4, 5, 7];

# Get the name of the sheet
sheet = list(all_data)[7]

# Get data from the specified sheet
sub_data = all_data[sheet]

# Get an inital number to plot
sub_data = sub_data.iloc[0:1]

# Get the column names of the plotted area
columns = []
for i in column_num:
    columns.append(list(sub_data)[i])

plot_data = sub_data[columns]


# Get the maximum data to set the layout
x_range, y_range, z_range = get_ranges(all_data, columns[1], columns[2],columns[5])


# Initialze graph
out_figure = update_plot(plot_data, None, 'linear', 'linear', 1, x_range, y_range, z_range)
out_style = dict(height = '100%', width = '100%')
animate = True

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
                    id = 'example-1-slider',
                    min = slider_min,
                    max = slider_max,
                    marks = slider_marks,
                    value = 7,
                    updatemode = 'mouseup'
                    )
            ],
            id = 'example-1-slider-call',
            className = 'slider'
        )
    ],
    width = dict(size = 6, offset = 3),
    id = 'example-1-filter-slider'
)

##==================================
## Dropdowns
##==================================
# Get labels
labels, size_labels = get_labels(sub_data)

# Set options
options = [{'label': i, 'value': i} for i in labels]
size_options = [{'label': i, 'value': i} for i in size_labels]
initial_values = columns[1:]

##==================================
## Size Axis
##==================================
size_axis = format_size([plot_data.iloc[:,4].min(), plot_data.iloc[:,4].max()])
min_size = size_axis[0]
max_size = size_axis[1]

##==================================
## Interval update
##==================================
interval = dcc.Interval(
    id='example-1-interval',
    interval=3000, # in milliseconds
    n_intervals=1
)

##==================================
## Assemble layout
##==================================
out = [
    app_navbar.get(),
    top_row.get(),
    size_scale.get(min_size, max_size),
    graph.get(out_style, out_figure, configure_graph),
    axis_select.get(options, size_options, initial_values),
    slider,
    data_table.get_table('example-1-data-table-plot'),
    interval,
    html.Div([],id='example-1-lastplot',style=dict(display = 'none')),
    html.Div(genSession(),id='example-1-session-id', style=dict(display='none')),
]

def layout():
    return out
