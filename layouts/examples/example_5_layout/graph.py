import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go


def get(out_style, out_figure, out_style_2, out_figure_2, configure_graph):
    out_graph = dcc.Graph(
        id = 'example-5-graph',
        config = configure_graph,
        figure = out_figure,
        style = out_style,
        animate = False
    )

    out_graph_2 = dcc.Graph(
        id = 'example-5-graph-2',
        config = configure_graph,
        figure = out_figure_2,
        style = out_style_2,
        animate = False
    )

    # Draw starting graph
    out = html.Div(
        [
            out_graph,
            out_graph_2
        ],
        id ='example-5-graph-container'
    )
    return out
