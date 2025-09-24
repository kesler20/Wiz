import os
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo, data_table
from layouts.examples.example_5_layout import app_navbar, graph, axis_select, top_row

import pandas as pd
from functions.example_5.data import *
from functions.example_5.graph import *

import static_datasets.datasets as glob_data

##==================================
## Global data
##==================================
# Get data
all_data = glob_data.example_5

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
                    id = 'example-5-slider',
                    min = slider_min,
                    max = slider_max,
                    marks = slider_marks,
                    value = 0,
                    updatemode = 'mouseup'
                )
            ],
            id = 'example-5-slider-call',
            className = 'slider'
        )
    ],
    width = dict(size = 6, offset = 3),
    id = 'example-5-filter-slider'
)

##==================================
## Initial data that is plotted
##==================================
# Analysis Type
analysis_type = 1;
class_select = None
click_data = None

# Get the name of the sheet
sheet = list(all_data)[0]

# Get data from the specified sheet
plot_data = all_data[sheet]


# Do analysis and plot based on the input type
if analysis_type == 1:
    # Analysis
    Y, var_exp, cum_var_exp = PCA(plot_data, class_select)

    # Get figuress
    out_style, out_figure, animate = PCA_plot(Y, plot_data, var_exp, cum_var_exp, class_select, click_data)
    out_style_2, out_figure_2 = PCA_plot_2(var_exp, cum_var_exp)

else:
    # Analysis
    Y_lda, var_exp, cum_var_exp = LDA(plot_data, class_select)

    # Determine figure type from data
    out_style, out_figure, animate = LDA_plot(Y_lda, plot_data, var_exp, cum_var_exp, class_select)
    out_style_2, out_figure_2 = LDA_plot_2(var_exp, cum_var_exp)

# Configuration for figure
configure_graph = graph_configure('hover')

##==================================
## Dropdowns
##==================================
# Get labels
class_options = get_labels(plot_data)

# Set options
options = [{'label': i, 'value': i} for i in class_options]

##==================================
## Assemble layout
##==================================
out = [
    app_navbar.get(),
    top_row.get(),
    graph.get(out_style, out_figure, out_style_2, out_figure_2, configure_graph),
    axis_select.get(options),
    slider,
    html.Div(genSession(),id='example-5-session-id', style=dict(display='none')),
]

def layout():
    return out
