import os
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo, data_table
from layouts.examples.example_3_layout import app_navbar, graph, axis_select

import pandas as pd
from functions.example_3.data import *
from functions.example_3.graph import *

import static_datasets.datasets as glob_data

##==================================
## Global data
##==================================
# Get data
df = glob_data.example_3

##==================================
## Slider
##==================================
# Populate the slider bar with the sheet options
years = range(2010, 2021)

slider_marks = {i : str(i) for i in years}
slider_min = years[0]
slider_max = years[-1]

slider = dbc.Col(
    [
        html.Div(
            [
                dcc.RangeSlider(
                    id = 'example-3-slider',
                    min = slider_min,
                    max = slider_max,
                    marks = slider_marks,
                    value = [slider_max-2, slider_max],
                    updatemode = 'mouseup'
                )
            ],
            id = 'example-3-slider-call',
            className = 'slider'
        )
    ],
    width = dict(size = 6, offset = 3),
    id = 'example-3-filter-slider'
)

##==================================
## Initial data that is plotted
##==================================
# Filter data based on range selected
df = df[(df['Date'] > str(slider_max - 2) + '-01-01') & (df['Date'] < str(slider_max + 1) + '-01-01')]

# DataType
datatype = 1;

# Get the column names of the plotted area
column_nums = [0, 1, 3, 5, 6]
columns = []
for i in column_nums:
    columns.append(list(df)[i])

plot_data = df[columns]


# Initialze graph
out_style, out_figure, animate = update_plot(plot_data, columns, None, 'linear', 'linear', datatype)

# Configuration for figure
configure_graph = graph_configure()

##==================================
## Dropdowns
##==================================
# Get labels
x_labels, y_labels, size_labels = get_labels(df, datatype)

# Set options
options = [{'label': i, 'value': i} for i in y_labels]
initial_values = columns[1:]

##==================================
## Assemble layout
##==================================
out = [
    app_navbar.get(),
    html.Br(),
    graph.get(out_style, out_figure, configure_graph),
    axis_select.get(options, initial_values),
    slider,
    html.Div(genSession(),id='example-3-session-id', style=dict(display='none')),
]

def layout():
    return out
