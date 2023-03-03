##==================================
## External imports
##==================================
import os
import base64
import io
import uuid
from math import log10
import pandas as pd
import json
import urllib
import plotly.graph_objs as go

##==================================
## Internal imports
##==================================
from functions.global_functions import *
from functions.example_1.data import *

##==================================
## General functions
##==================================
def graph_configure():
    return dict(
        displayModeBar = 'hover',
        showSendToCloud = False,
        toImageButtonOptions = dict(
            format = 'svg',
        ),
        displaylogo = False,
        watermark = False,
        responsive = True,
    )

def update_plot(plot_data, click_data, x_type, y_type, graph_type, x_range, y_range, z_range):
    # Different plots depending on user data selection
    if graph_type == 1:
        # Use WebGL for larger datasets
        if len(plot_data) > 2500:
            out_figure = figure = dict(
              data = scatter_2D_dataGL(plot_data),
              layout = scatter_2D_layout(plot_data, x_type, y_type, click_data, x_range, y_range)
            )
        else:
            out_figure = figure = dict(
              data = scatter_2D_data(plot_data),
              layout = scatter_2D_layout(plot_data, x_type, y_type, click_data, x_range, y_range)
            )


    # If it's 3D then hide the 2D graph and display the 3D graph
    if graph_type == 2:

        out_figure = figure = dict(
          data = scatter_3D_data(plot_data),
          layout = scatter_3D_layout(plot_data, x_type, y_type, x_range, y_range, z_range),
        )

    return out_figure

##==================================
## 2D Scatter
##==================================
def axis_layout_2D(column_info, type, axis_range):
    title = column_info[0]

    axis_layout = dict(
        title = '<b>' + title + '<b>',
        showline = True,
        linewidth  = AXIS_LINE_WIDTH,
        linecolor  = AXIS_LINE_COLOR,
        mirror     = True,
        ticks = 'outside',
        showgrid = False,
        zeroline = False,
        autorange = True,
        automargin = True,
        titlefont = dict(
            family = FONT_FAMILY['plot_labels'],
            size = FONT_SIZE['plot_labels'],
        )
    )

    if 'float' in column_info[1] or 'int' in column_info[1]:
        axis_layout.update(dict(type = type, nticks = 5))

    if len(axis_range) > 0:
        axis_layout.update(dict(autorange = False, range = axis_range))

    return axis_layout

def scatter_2D_layout(df_clean, x_type, y_type, click_data, x_range, y_range):
    # Number of variables
    n_var = len(list(df_clean)) - 1

    label_column = list(df_clean)[0]
    x_column = [list(df_clean)[1], df_clean.dtypes[1].name]
    y_column = [list(df_clean)[2], df_clean.dtypes[2].name]

    # Set up annotations
    annotation = [];
    if click_data is not None:
        # Get the label and x/y info
        name_text = click_data['points'][0]['text']
        x_loc = click_data['points'][0]['x']
        y_loc = click_data['points'][0]['y']
        x_text = str(x_loc)
        y_text = str(y_loc)

        # Change label location if the axis is Log
        if x_type == 'log' and isinstance(x_loc, str) == 0:
            x_loc = log10(x_loc)
        if y_type == 'log' and isinstance(y_loc, str) == 0:
            y_loc = log10(y_loc)

        # Check if color and size need to be in the annotation
        if 'marker.color' in click_data['points'][0]:
            color_text = str(click_data['points'][0]['marker.color'])
            c_column = list(df_clean)[3]
            color_anno = c_column + ': ' + color_text + '<br>'
        else:
            color_anno = ''

        if n_var == 4:
            if 'marker.size' in click_data['points'][0]:
                s_column = list(df_clean)[4]
                size_index = df_clean.index[df_clean[label_column] == name_text][0]
                size_text = str(df_clean.at[size_index, s_column])
                size_anno = s_column + ': ' + size_text + '<br>'
            else:
                size_anno = ''
        else:
            size_anno = ''

        # Create annotation
        annotation_text = dict(
            x = x_loc,
            y = y_loc,
            align = 'right',
            ax = 180,
            ay = 20,
            bgcolor = '#666666',
            opacity = OPACITY,
            font = dict(color = 'white'),
            showarrow = True,
            arrowhead = 7,
            arrowsize = 1,
            arrowwidth = 2,
            clicktoshow = 'onout',
            text = '<b>' + str(name_text) + '</b><br>' +
                x_column[0] + ': ' + x_text + '<br>' + y_column[0] + ': ' +
                y_text + '<br>' + color_anno + size_anno
            )
        annotation.append(annotation_text)

    return go.Layout(
            autosize = True,
            xaxis = axis_layout_2D(x_column, x_type, x_range),
            yaxis = axis_layout_2D(y_column, y_type, y_range),
            annotations = annotation,
            font =  dict(
                family = FONT_FAMILY['plot'],
                size = FONT_SIZE['plot'],
            ),
            hovermode = 'closest',
            margin = dict(l = 50, b = 40, t = 10, r = 30),
            uirevision='foo',
            legend=dict(x=1.02, y=0.98),
            template = TEMPLATE
        )

def scatter_2D_data(df_clean):
    # Number of variables
    n_var = len(list(df_clean)) - 1

    # Names of columns in array
    mof_column = list(df_clean)[0]
    x_column = list(df_clean)[1]
    y_column = list(df_clean)[2]

    # Default size
    size = [25 for i in range(len(df_clean.iloc[:,0]))]

    # Plot x and y if they are the only ones defined
    if n_var == 2:
        traces = [go.Scatter(
            x = df_clean.iloc[:,1],
            y = df_clean.iloc[:,2],
            mode = 'markers',
            text = df_clean.iloc[:,0],
            name = 'Label',
            opacity = OPACITY,
            hoverinfo = 'text',
            marker = dict(
                size = size,
                sizemode = 'diameter',
                line = dict(
                    width = 0.5,
                    color = 'white'
                ),
            )
        )]

    # Plot with colors and size if specified
    elif n_var >= 3:
        # Get color column name
        c_column = list(df_clean)[3]

        # Set size if the size variable is selected
        if n_var >= 4:
            size = normalize_size(df_clean.iloc[:,4])

        # Determine if color data is categorical then plot
        if 'float' in df_clean.dtypes[3].name or 'int' in df_clean.dtypes[3].name:
            traces = [go.Scatter(
                x = df_clean.iloc[:,1],
                y = df_clean.iloc[:,2],
                mode = 'markers',
                text = df_clean.iloc[:,0],
                name = 'Label',
                opacity = OPACITY,
                hoverinfo = 'text',
                marker = dict(
                    size = size,
                    sizemode = 'diameter',
                    color = df_clean.iloc[:,3],
                    colorscale = COLORSCALE,
                    line = dict(
                        width = 0.5,
                        color = 'white'
                    ),
                    colorbar = dict(
                        title = '<b>' + c_column + '<b>',
                        titleside = 'right',
                        titlefont = dict(
                            family = FONT_FAMILY['plot_labels'],
                            size = FONT_SIZE['plot_labels'],
                        )
                    )
                )
            )]

        else:
            traces = []
            for i in df_clean.iloc[:,3].unique():
                df_by_color = df_clean[df_clean[c_column] == i]

                # Set size if the size variable is selected
                if n_var > 3:
                    size = normalize_size(df_by_color.iloc[:,4])

                # Add categorical trace
                traces.append(
                    go.Scatter(
                        x = df_by_color.iloc[:,1],
                        y = df_by_color.iloc[:,2],
                        mode = 'markers',
                        text = df_by_color.iloc[:,0],
                        name = str(i),
                        opacity = OPACITY,
                        hoverinfo = 'text',
                        marker = dict(
                            size = size,
                            sizemode = 'diameter',
                            colorscale = COLORSCALE,
                            line = dict(
                                width = 0.5,
                                color = 'white'
                            ),
                        )
                    )
                )

    return traces

def scatter_2D_dataGL(df_clean):
    # Number of variables
    n_var = len(list(df_clean)) - 1

    # Names of columns in array
    mof_column = list(df_clean)[0]
    x_column = list(df_clean)[1]
    y_column = list(df_clean)[2]

    # Default size
    size = [25 for i in range(len(df_clean.iloc[:,0]))]

    # Plot x and y if they are the only ones defined
    if n_var == 2:
        traces = [go.Scattergl(
            x = df_clean.iloc[:,1],
            y = df_clean.iloc[:,2],
            mode = 'markers',
            text = df_clean.iloc[:,0],
            name = 'Label',
            opacity = OPACITY,
            hoverinfo = 'text',
            marker = dict(
                size = size,
                sizemode = 'diameter',
                line = dict(
                    width = 0.5,
                    color = 'white'
                ),
            )
        )]

    # Plot with colors and size if specified
    elif n_var >= 3:
        # Get color column name
        c_column = list(df_clean)[3]

        # Set size if the size variable is selected
        if n_var >= 4:
            size = normalize_size(df_clean.iloc[:,4])

        # Determine if color data is categorical then plot
        if 'float' in df_clean.dtypes[3].name or 'int' in df_clean.dtypes[3].name:
            traces = [go.Scatter(
                x = df_clean.iloc[:,1],
                y = df_clean.iloc[:,2],
                mode = 'markers',
                text = df_clean.iloc[:,0],
                name = 'Label',
                opacity = OPACITY,
                hoverinfo = 'text',
                marker = dict(
                    size = size,
                    sizemode = 'diameter',
                    color = df_clean.iloc[:,3],
                    colorscale = COLORSCALE,
                    line = dict(
                        width = 0.5,
                        color = 'white'
                    ),
                    colorbar = dict(
                        title = '<b>' + c_column + '<b>',
                        titleside = 'right',
                        titlefont = dict(
                            family = FONT_FAMILY['plot_labels'],
                            size = FONT_SIZE['plot_labels'],
                        )
                    )
                )
            )]

        else:
            traces = []
            for i in df_clean.iloc[:,3].unique():
                df_by_color = df_clean[df_clean[c_column] == i]

                # Set size if the size variable is selected
                if n_var > 3:
                    size = normalize_size(df_by_color.iloc[:,4])

                # Add categorical trace
                traces.append(
                    go.Scatter(
                        x = df_by_color.iloc[:,1],
                        y = df_by_color.iloc[:,2],
                        mode = 'markers',
                        text = df_by_color.iloc[:,0],
                        name = str(i),
                        opacity = OPACITY,
                        hoverinfo = 'text',
                        marker = dict(
                            size = size,
                            sizemode = 'diameter',
                            colorscale = COLORSCALE,
                            line = dict(
                                width = 0.5,
                                color = 'white'
                            ),
                        )
                    )
                )

    return traces


##==================================
## 3D Scatter
##==================================
def axis_layout_3D(column_info, type, axis_range):
    title = column_info[0]

    axis_layout = dict(
        title = title,
        zeroline = False,
        autorange = True,
        titlefont = dict(
            family = FONT_FAMILY['plot_labels'],
            size = FONT_SIZE['plot_labels']*3/4,
        ),
    )

    if 'float' in column_info[1]:
        axis_layout.update(dict(type = type, nticks = 5))

    if len(axis_range) > 0:
        axis_layout.update(dict(autorange = False, range = axis_range))

    return axis_layout


def scatter_3D_layout(df_clean, x_type, y_type, x_range, y_range, z_range):
    mof_column = list(df_clean)[0]
    x_column = [list(df_clean)[1], df_clean.dtypes[1].name]
    y_column = [list(df_clean)[2], df_clean.dtypes[2].name]
    z_column = [list(df_clean)[5], df_clean.dtypes[5].name]
    return go.Layout(
        font =  dict(
            family = FONT_FAMILY['plot'],
            size = FONT_SIZE['plot']*3/4,
        ),
        hovermode = 'closest',
        margin = dict(l = 0, b = 0, t = 0, r = 0),
        scene = dict(
            aspectratio = dict(
                x = 2,
                y = 2,
                z = 1
            ),
            xaxis = axis_layout_3D(x_column, x_type, x_range),
            yaxis = axis_layout_3D(y_column, y_type, y_range),
            zaxis = axis_layout_3D(z_column, 'linear', z_range),
        ),
        uirevision='foo',
        legend=dict(x=1.02, y=0.95),
        template = TEMPLATE
    )


def scatter_3D_data(df_clean):
    mof_column = list(df_clean)[0]
    x_column = list(df_clean)[1]
    y_column = list(df_clean)[2]
    c_column = list(df_clean)[3]
    s_column = list(df_clean)[4]
    z_column = list(df_clean)[5]

    if 'float' in df_clean.dtypes[3].name or 'int' in df_clean.dtypes[3].name:
        traces = [
            go.Scatter3d(
                x = df_clean.iloc[:,1],
                y = df_clean.iloc[:,2],
                z = df_clean.iloc[:,5],
                mode = 'markers',
                text = df_clean.iloc[:,0],
                name = 'Label',
                # opacity = OPACITY;,
                hoverinfo = 'text',
                hoverlabel  = dict(
                    bgcolor = 'lightgray'
                ),
                marker = dict(
                    size = normalize_size(df_clean.iloc[:,4]),
                    sizemode = 'diameter',
                    color = df_clean.iloc[:,3],
                    colorscale = COLORSCALE,
                    line = dict(
                        width = 0,
                    ),
                    colorbar = dict(
                        title = '<b>' + c_column + '<b>',
                        titleside = 'right',
                        titlefont = dict(
                            family = FONT_FAMILY['plot_labels'],
                            size = FONT_SIZE['plot_labels'],
                        )
                    )
                )
            )
        ]

    else:
        traces = []
        for i in df_clean.iloc[:,3].unique():
            df_by_color = df_clean[df_clean[c_column] == i]

            traces.append(go.Scatter3d(
                x = df_by_color.iloc[:,1],
                y = df_by_color.iloc[:,2],
                z = df_clean.iloc[:,5],
                mode = 'markers',
                text = df_by_color.iloc[:,0],
                name = str(i),
                opacity = OPACITY,
                hoverinfo = 'text',
                hoverlabel  = dict(
                    bgcolor = 'lightgray'
                    ),
                marker = dict(
                    size = normalize_size(df_clean.iloc[:,4]),
                    sizemode = 'diameter',
                    colorscale = COLORSCALE,
                    line = dict(
                        width = 0.00,
                    ),
                )
            )
            )

    return traces

# If it is run as the main function
if __name__ == '__main__':
    print('')
