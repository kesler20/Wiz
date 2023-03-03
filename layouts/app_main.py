import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from layouts.global_layout import bubble_nav_logo, data_table
from layouts.app_main_layout import app_navbar, top_row, size_scale, graph, axis_select, sheet_slider, help_dialog
from functions.global_functions import genSession

##==================================
## Assemble layout
##==================================
out = [
    app_navbar.get(),
    top_row.get(),
    size_scale.get(),
    graph.get(),
    axis_select.get(),
    sheet_slider.get(),
    help_dialog.get(),
    data_table.get('main'),
    html.Div(id='main-session-id', style=dict(display='none')),
    html.Div(id='main-graph-timestamp', style=dict(display='none')),
    html.Div(id='main-table-timestamp', style=dict(display='none')),
    html.Div(id='main-table-filter', style=dict(display='none')),
    html.Div(id='main-table-selected-rows', style=dict(display='none')),
]

def layout():
    return out
