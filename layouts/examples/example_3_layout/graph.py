from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd


def get(out_style, out_figure, configure_graph):
    out_graph = dcc.Graph(
        id = 'example-3-graph',
        config = configure_graph,
        figure = out_figure,
        style = out_style,
        animate = True
    )

    # Draw starting graph
    out = html.Div(
        [
            out_graph
        ],
        id ='example-3-graph-container'
    )
    return out

def get_graph():
    return out_graph
