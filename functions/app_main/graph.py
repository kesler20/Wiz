##==================================
## External imports
##==================================
import os
import base64
import io
import uuid
from math import log10
from numpy import linspace, array
from numpy import append as ap
from itertools import compress
import pandas as pd
import json
import urllib
import plotly.graph_objs as go
##==================================
## Internal imports
##==================================
from functions.global_functions import *
from functions.app_main.data import *

##==================================
## General functions
##==================================
def graph_configure(modeBar):
    if type(modeBar) is bool:
        editable = modeBar
    else:
        if 'hover' in modeBar:
            editable = True
        else:
            editable = False

    return dict(
        displayModeBar = modeBar,
        showSendToCloud = False,
        toImageButtonOptions = dict(
            format = 'svg',
        ),
        displaylogo = False,
        watermark = False,
        responsive = True,
        editable = editable,
        edits = dict(
            titleText = False,
        )
    )

def pick_plot(plot_data, columns, click_data, x_type, y_type, graph_type):
    # If no data columns are selected, then output a blank layout
    if columns is None or columns == [] or plot_data is None:
        out_figure = dict(data = [], layout = blank_layout())
        animate = False
    # If no data columns are selected, then output a blank layout
    elif len(columns) == 1 or len(list(plot_data)) == 0:
        out_figure = dict(data = [], layout = blank_layout())
        animate = False
    # If one column of data is selected, then plot a histrogram
    elif len(columns) == 2:
        out_figure = figure = dict(
          data = histogram_data(plot_data),
          layout = histogram_layout(plot_data)
        )
        animate = False
    else:
        # Different plots depending on user data selection
        if graph_type == 1:

            # Use WebGL for larger datasets
            if len(plot_data) > WEBGL_CUTOFF:
                out_figure = dict(
                  data = scatter_2D_dataGL(plot_data),
                  layout = scatter_2D_layout(plot_data, x_type, y_type, click_data)
                )
            else:
                out_figure = dict(
                  data = scatter_2D_data(plot_data),
                  layout = scatter_2D_layout(plot_data, x_type, y_type, click_data)
                )

            # Animate transitions plots (currently off)
            if len(columns) > 3:
                animate = False
            else:
                animate = False

        # 3D Scatter plot
        if graph_type == 2:
            out_figure = dict(
              data = scatter_3D_data(plot_data),
              layout = scatter_3D_layout(plot_data, x_type, y_type),
            )
            animate = False

    # Return a default style (this could be updated to be specific for plot types)
    out_style = dict(height = '100%', width = '100%')
    return out_style, out_figure, animate

##==================================
## Blank layout
##==================================
def blank_layout():
    return go.Layout(
        title = dict(text = ' '),
        xaxis = dict(
            autorange      = True,
            showgrid       = False,
            zeroline       = False,
            showline       = False,
            ticks          = '',
            showticklabels = False
        ),
        yaxis = dict(
            autorange      = True,
            showgrid       = False,
            zeroline       = False,
            showline       = False,
            ticks          = '',
            showticklabels =False
        ),
    )

##==================================
## Histogram
##==================================
def histogram_data(df_clean):
    # Data
    count_data = df_clean.iloc[:,1]

    # Call graph
    trace = go.Histogram(
        x       = count_data,
        opacity = OPACITY,
        name    = list(df_clean)[0]
    )
    return [trace]

def histogram_layout(df_clean):
    return go.Layout(
        font    = dict(
            family = FONT_FAMILY['plot'],
            size   = FONT_SIZE['plot'],
        ),
        margin  = dict(
            t = 5,
            r = 5,
        ),
        bargap  = 0.2,
        xaxis   = dict(
            title      = '<b>' + list(df_clean)[1] + '<b>',
            showline   = True,
            linewidth  = AXIS_LINE_WIDTH,
            linecolor  = AXIS_LINE_COLOR,
            mirror     = True,
            ticks      = 'outside',
            zeroline   = False,
            automargin = True,
            autorange  = True,
            titlefont  = dict(
                family = FONT_FAMILY['plot_labels'],
                size   = FONT_SIZE['plot_labels'],
            )
        ),
        yaxis   = dict(
            title      = '<b>' + 'Count' + '<b>',
            showline   = True,
            linewidth  = AXIS_LINE_WIDTH,
            linecolor  = AXIS_LINE_COLOR,
            mirror     = True,
            ticks      = 'outside',
            zeroline   = False,
            automargin = True,
            autorange  = True,
            titlefont  = dict(
                family = FONT_FAMILY['plot_labels'],
                size   = FONT_SIZE['plot_labels'],
            )
        ),
        template    = TEMPLATE
    )

##==================================
## 2D Scatter
##==================================
def axis_layout_2D(column_info, type):
    title = column_info[0]

    axis_layout = dict(
        title      = '<b>' + title + '<b>',
        showline   = True,
        linewidth  = AXIS_LINE_WIDTH,
        linecolor  = AXIS_LINE_COLOR,
        mirror     = True,
        ticks      = 'outside',
        showgrid   = False,
        zeroline   = False,
        autorange  = True,
        automargin = True,
        titlefont  = dict(
            family = FONT_FAMILY['plot_labels'],
            size   = FONT_SIZE['plot_labels'],
        )
    )

    # If there are floats or ints, then change the axis if log
    if 'float' in column_info[1] or 'int' in column_info[1]:
        axis_layout.update(dict(type = type, nticks = 5))

    return axis_layout

def scatter_2D_layout(df_clean, x_type, y_type, click_data):
    # Number of data columns
    n_var = len(list(df_clean)) - 1

    # Get names of columns (and type of data)
    label_column = list(df_clean)[0]
    x_column     = [list(df_clean)[1], df_clean.dtypes[1].name]
    y_column     = [list(df_clean)[2], df_clean.dtypes[2].name]

    # Create click annotation
    annotation = [];
    if click_data is not None:
        # Get the label and x/y info
        name_text = click_data['points'][0]['text']
        x_loc     = click_data['points'][0]['x']
        y_loc     = click_data['points'][0]['y']
        x_text    = str(x_loc)
        y_text    = str(y_loc)

        # Change label location if the axis is Log
        if x_type == 'log' and isinstance(x_loc, str) == 0:
            x_loc = log10(x_loc)
        if y_type == 'log' and isinstance(y_loc, str) == 0:
            y_loc = log10(y_loc)

        # Check if color and size need to be in the annotation
        if 'marker.color' in click_data['points'][0]:
            color_text = str(click_data['points'][0]['marker.color'])
            c_column   = list(df_clean)[3]
            color_anno = c_column + ': ' + color_text + '<br>'
        else:
            color_anno = ''

        if n_var == 4:
            if 'marker.size' in click_data['points'][0]:
                s_column   = list(df_clean)[4]
                size_index = df_clean.index[df_clean[label_column] == name_text][0]
                size_text  = str(df_clean.at[size_index, list(df_clean)[4]])
                size_anno  = s_column + ': ' + size_text + '<br>'
            else:
                size_anno = ''
        else:
            size_anno = ''

        # Create annotation
        annotation_text = dict(
            x           = x_loc,
            y           = y_loc,
            align       = 'right',
            ax          = 180,
            ay          = 20,
            bgcolor     = '#666666',
            opacity     = OPACITY,
            font        = dict(color = 'white'),
            showarrow   = True,
            arrowhead   = 7,
            arrowsize   = 1,
            arrowwidth  = 2,
            clicktoshow = 'onout',
            text        = '<b>' + str(name_text) + '</b><br>' +
                x_column[0] + ': ' + x_text + '<br>' + y_column[0] + ': ' +
                y_text + '<br>' + color_anno + size_anno
            )
        annotation.append(annotation_text)

    return go.Layout(
            autosize    = True,
            title       = dict(text = ' '),
            xaxis       = axis_layout_2D(x_column, x_type),
            yaxis       = axis_layout_2D(y_column, y_type),
            annotations = annotation,
            font        = dict(
                family = FONT_FAMILY['plot'],
                size   = FONT_SIZE['plot'],
            ),
            hovermode   = 'closest',
            margin      = dict(l = 50, b = 40, t = 10, r = 30),
            uirevision  ='foo',
            legend      = dict(x=1.02, y=0.98),
            template    = TEMPLATE
        )

def scatter_2D_data(df_clean):
    # Number of data columns
    n_var = len(list(df_clean)) - 1

    # Names of columns in array
    label_column = list(df_clean)[0]
    x_column     = list(df_clean)[1]
    y_column     = list(df_clean)[2]

    # Check if x is categorical
    x_not_cat = 'float' in df_clean.dtypes[1].name or ('int' in df_clean.dtypes[1].name and df_clean[x_column].unique().shape[0] > MAX_CAT_INTS)

    # Default size
    size = DEFAULT_BUBBLE_SIZE

    # Plot x and y if they are the only ones defined
    if n_var == 2:
        if x_not_cat:
            traces = [
                go.Scatter(
                    x         = df_clean.iloc[:,1],
                    y         = df_clean.iloc[:,2],
                    mode      = 'markers',
                    text      = df_clean.iloc[:,0],
                    name      = 'Label',
                    opacity   = OPACITY,
                    hoverinfo = 'text',
                    marker    = dict(
                        size     = size,
                        opacity  = OPACITY,
                        sizemode = 'diameter',
                        line     = dict(
                            width = 0.5,
                            color = 'white'
                        ),
                    )
                )
            ]
        else:
            traces = []
            for i in df_clean.iloc[:,1].unique():
                # Filter each unique value for x
                df_by_x = df_clean[df_clean[x_column] == i]
                df_by_x.reset_index(inplace = True, drop = True)

                # Add categorical trace
                traces.append(
                    go.Box(
                        y         = df_by_x.iloc[:,2],
                        text      = df_by_x.iloc[:,0],
                        boxpoints ='all',
                        jitter    = 0.5,
                        pointpos  = -1.5,
                        name      = str(i),
                        opacity   = OPACITY,
                        hoverinfo = 'x+y+text',
                        marker    = dict(
                            size = 10,
                            line = dict(
                                width = 0.5,
                                color = 'white'
                            ),
                        )
                    )
                )

    # Plot with colors and size if specified
    elif n_var >= 3:
        # Get color column name
        c_column = list(df_clean)[3]

        # Check if color is a categorical variable
        color_not_cat = 'float' in df_clean.dtypes[3].name or ('int' in df_clean.dtypes[3].name and df_clean[c_column].unique().shape[0] > 20)

        # Set size if the size variable is selected
        if n_var == 4:
            size = normalize_size(df_clean.iloc[:,4])

        # Determine if color data is categorical then plot
        x_not_cat = True  # Until the color is fixed (cannot do categorical color for boxplots yet!)
        if x_not_cat == False:
            # Get new list of colors that are RGB
            color_bins = 5
            c          = ['hsl('+str(h)+',50%'+',50%)' for h in linspace(0, 360, color_bins)]

            # Loop through sorted color data and divide into bins
            new_colors = []
            temp_min   = df_clean.iloc[:,3].min();
            temp_max   = df_clean.iloc[:,3].max();

            for i in df_clean.iloc[:,3]:
                temp = abs(round((i - temp_min)/(temp_min-temp_max)*color_bins))
                new_colors.append(temp)


            traces = []
            for i in df_clean.iloc[:,1].unique():
                # Filter each unique value for x
                filter_values = df_clean[x_column] == i;
                df_by_x       = df_clean[filter_values]

                filtered_colors   = list(compress(new_colors, filter_values.tolist()))
                filtered_colors_2 = array([])
                for n in filtered_colors:
                    filtered_colors_2 = ap(filtered_colors_2, [float(n) + 0.5])

                # Add categorical trace
                traces.append(
                    go.Box(
                        y         = df_by_x.iloc[:,2],
                        text      = df_by_x.iloc[:,0],
                        boxpoints ='x+y+all',
                        jitter    = 0.5,
                        pointpos  = -1.5,
                        name      = str(i),
                        opacity   = OPACITY,
                        hoverinfo = 'text',
                        marker    = dict(
                            size  = 10,
                        )
                    )
                )
        elif color_not_cat:
            traces = [
                go.Scatter(
                    x         = df_clean.iloc[:,1],
                    y         = df_clean.iloc[:,2],
                    mode      = 'markers',
                    text      = df_clean.iloc[:,0],
                    name      = 'Label',
                    opacity   = OPACITY,
                    hoverinfo = 'text',
                    marker    = dict(
                        size       = size,
                        opacity    = OPACITY,
                        sizemode   = 'diameter',
                        color      = df_clean.iloc[:,3],
                        colorscale = COLORSCALE,
                        line       = dict(
                            width  = 0.5,
                            color  = 'white'
                        ),
                        colorbar = dict(
                            title     = '<b>' + c_column + '<b>',
                            titleside = 'right',
                            titlefont = dict(
                                family = FONT_FAMILY['plot_labels'],
                                size   = FONT_SIZE['plot_labels'],
                            )
                        )
                    )
                )
            ]

        else:
            traces = []
            for i in df_clean.iloc[:,3].unique():
                df_by_color = df_clean[df_clean[c_column] == i]
                df_by_color.reset_index(inplace = True, drop = True)

                # Set size if the size variable is selected
                if n_var > 3:
                    size = normalize_size(df_by_color.iloc[:,4])

                # Add categorical trace
                traces.append(
                    go.Scatter(
                        x         = df_by_color.iloc[:,1],
                        y         = df_by_color.iloc[:,2],
                        mode      = 'markers',
                        text      = df_by_color.iloc[:,0],
                        name      = str(i),
                        opacity   = OPACITY,
                        hoverinfo = 'text',
                        marker    = dict(
                            size       = size,
                            opacity    = OPACITY,
                            sizemode   = 'diameter',
                            colorscale = COLORSCALE,
                            line       = dict(
                                width  = 0.5,
                                color  = 'white'
                            ),
                        )
                    )
                )

    return traces

def scatter_2D_dataGL(df_clean):
    # Number of data columns
    n_var = len(list(df_clean)) - 1

    # Names of columns in array
    label_column = list(df_clean)[0]
    x_column     = list(df_clean)[1]
    y_column     = list(df_clean)[2]

    # Check if x is categorical
    x_not_cat = 'float' in df_clean.dtypes[1].name or ('int' in df_clean.dtypes[1].name and df_clean[x_column].unique().shape[0] > MAX_CAT_INTS)

    # Default size
    size = DEFAULT_BUBBLE_SIZE

    # Plot x and y if they are the only ones defined
    if n_var == 2:
        if x_not_cat:
            traces = [
                go.Scattergl(
                    x         = df_clean.iloc[:,1],
                    y         = df_clean.iloc[:,2],
                    mode      = 'markers',
                    text      = df_clean.iloc[:,0],
                    name      = 'Label',
                    hoverinfo = 'text',
                    marker    = dict(
                        size     = size,
                        opacity  = 1.0,
                        sizemode = 'diameter',
                        line     = dict(
                            width = 0.5,
                            color = 'black'
                        ),
                    )
                )
            ]
        else:
            traces = []
            for i in df_clean.iloc[:,1].unique():
                # Filter each unique value for x
                df_by_x = df_clean[df_clean[x_column] == i]
                df_by_x.reset_index(inplace = True, drop = True)

                # Add categorical trace
                traces.append(
                    # go.Box(
                    #     y         = df_by_x.iloc[:,2],
                    #     text      = df_by_x.iloc[:,0],
                    #     boxpoints = False,
                    #     jitter    = 0.5,
                    #     pointpos  = -1.5,
                    #     name      = str(i),
                    #     opacity   = OPACITY,
                    #     hoverinfo = 'text',
                    #     marker    = dict(
                    #         size = 10,
                    #         line = dict(
                    #             width = 0.5,
                    #             color = 'white'
                    #         ),
                    #     )
                    # )
                    go.Violin(
                        y         = df_by_x.iloc[:,2],
                        text      = df_by_x.iloc[:,0],
                        name      = str(i),
                        box_visible=True,
                        meanline_visible=True,
                        hoverinfo = 'x+y+text',
                    )
                )

    # Plot with colors and size if specified
    elif n_var >= 3:
        # Get color column name
        c_column = list(df_clean)[3]

        # Check if color is a categorical variable
        color_not_cat = 'float' in df_clean.dtypes[3].name or ('int' in df_clean.dtypes[3].name and df_clean[c_column].unique().shape[0] > 20)

        # Set size if the size variable is selected
        if n_var == 4:
            size = normalize_size(df_clean.iloc[:,4])

        # Determine if color data is categorical then plot
        x_not_cat = True  # Until the color is fixed (cannot do categorical color for boxplots yet!)
        if x_not_cat == False:
            # Get new list of colors that are RGB
            color_bins = 5
            c          = ['hsl('+str(h)+',50%'+',50%)' for h in linspace(0, 360, color_bins)]

            # Loop through sorted color data and divide into bins
            new_colors = []
            temp_min   = df_clean.iloc[:,3].min();
            temp_max   = df_clean.iloc[:,3].max();

            for i in df_clean.iloc[:,3]:
                temp = abs(round((i - temp_min)/(temp_min-temp_max)*color_bins))
                new_colors.append(temp)


            traces = []
            for i in df_clean.iloc[:,1].unique():
                # Filter each unique value for x
                filter_values = df_clean[x_column] == i;
                df_by_x       = df_clean[filter_values]

                filtered_colors   = list(compress(new_colors, filter_values.tolist()))
                filtered_colors_2 = array([])
                for n in filtered_colors:
                    filtered_colors_2 = ap(filtered_colors_2, [float(n) + 0.5])

                # Add categorical trace
                traces.append(
                    go.Violin(
                        y         = df_by_x.iloc[:,2],
                        text      = df_by_x.iloc[:,0],
                        name      = str(i),
                        box_visible=True,
                        meanline_visible=True,
                        hoverinfo = 'x+y+text',
                    )
                )
        elif color_not_cat:
            traces = [
                go.Scattergl(
                    x          = df_clean.iloc[:,1],
                    y          = df_clean.iloc[:,2],
                    mode       = 'markers',
                    text       = df_clean.iloc[:,0],
                    name       = 'Label',
                    hoverinfo  = 'text',
                    hoverlabel = dict(
                        bgcolor = 'lightgray'
                    ),
                    marker     = dict(
                        size       = size,
                        opacity    = 1.0,
                        sizemode   = 'diameter',
                        color      = df_clean.iloc[:,3],
                        colorscale = COLORSCALE,
                        line       = dict(
                            width  = 0.5,
                            color  = 'black'
                        ),
                        colorbar = dict(
                            title     = '<b>' + c_column + '<b>',
                            titleside = 'right',
                            titlefont = dict(
                                family = FONT_FAMILY['plot_labels'],
                                size   = FONT_SIZE['plot_labels'],
                            )
                        )
                    )
                )
            ]

        else:
            traces = []
            for i in df_clean.iloc[:,3].unique():
                df_by_color = df_clean[df_clean[c_column] == i]
                df_by_color.reset_index(inplace = True, drop = True)

                # Set size if the size variable is selected
                if n_var > 3:
                    size = normalize_size(df_by_color.iloc[:,4])

                # Add categorical trace
                traces.append(
                    go.Scattergl(
                        x          = df_by_color.iloc[:,1],
                        y          = df_by_color.iloc[:,2],
                        mode       = 'markers',
                        text       = df_by_color.iloc[:,0],
                        name       = str(i),
                        hoverinfo  = 'text',
                        marker     = dict(
                            size       = size,
                            opacity    = 1.0,
                            sizemode   = 'diameter',
                            colorscale = COLORSCALE,
                            line       = dict(
                                width  = 0.5,
                                color  = 'black'
                            ),
                        )
                    )
                )

    return traces


##==================================
## 3D Scatter
##==================================
def axis_layout_3D(column_info, type):
    title = column_info[0]

    axis_layout = dict(
        title     = title,
        zeroline  = False,
        autorange = True,
        titlefont = dict(
            family = FONT_FAMILY['plot_labels'],
            size   = FONT_SIZE['plot_labels']*3/4,
        ),
    )

    if 'float' in column_info[1] or 'int' in column_info[1]:
        axis_layout.update(dict(type = type, nticks = 5))

    return axis_layout


def scatter_3D_layout(df_clean, x_type, y_type):
    lable_column = list(df_clean)[0]
    x_column     = [list(df_clean)[1], df_clean.dtypes[1].name]
    y_column     = [list(df_clean)[2], df_clean.dtypes[2].name]
    z_column     = [list(df_clean)[5], df_clean.dtypes[5].name]
    return go.Layout(
        font       =  dict(
            family = FONT_FAMILY['plot'],
            size   = FONT_SIZE['plot']*3/4,
        ),
        title      = dict(text = ' '),
        hovermode  = 'closest',
        margin     = dict(l = 0, b = 0, t = 0, r = 0),
        scene      = dict(
            aspectratio = dict(
                x = 2,
                y = 2,
                z = 1
            ),
            xaxis = axis_layout_3D(x_column, x_type),
            yaxis = axis_layout_3D(y_column, y_type),
            zaxis = axis_layout_3D(z_column, 'linear'),
        ),
        uirevision = 'foo',
        legend     = dict(x = 1.02, y = 0.95),
        template    = TEMPLATE,
    )


def scatter_3D_data(df_clean):
    # Get the axis names
    label_column = list(df_clean)[0]
    x_column     = list(df_clean)[1]
    y_column     = list(df_clean)[2]
    c_column     = list(df_clean)[3]
    s_column     = list(df_clean)[4]
    z_column     = list(df_clean)[5]

    if 'float' in df_clean.dtypes[3].name or 'int' in df_clean.dtypes[3].name:
        traces = [
            go.Scatter3d(
                x          = df_clean.iloc[:,1],
                y          = df_clean.iloc[:,2],
                z          = df_clean.iloc[:,5],
                mode       = 'markers',
                text       = df_clean.iloc[:,0],
                name       = 'Label',
                hoverinfo  = 'text',
                hoverlabel = dict(
                    bgcolor = 'lightgray'
                ),
                marker     = dict(
                    size       = normalize_size(df_clean.iloc[:,4]),
                    sizemode   = 'diameter',
                    color      = df_clean.iloc[:,3],
                    colorscale = COLORSCALE,
                    line       = dict(
                        width  = 0,
                    ),
                    colorbar = dict(
                        title     = '<b>' + c_column + '<b>',
                        titleside = 'right',
                        titlefont = dict(
                            family = FONT_FAMILY['plot_labels'],
                            size   = FONT_SIZE['plot_labels'],
                        )
                    )
                )
            )
        ]

    else:
        traces = []
        for i in df_clean.iloc[:,3].unique():
            df_by_color = df_clean[df_clean[c_column] == i]

            traces.append(
                go.Scatter3d(
                    x          = df_by_color.iloc[:,1],
                    y          = df_by_color.iloc[:,2],
                    z          = df_clean.iloc[:,5],
                    mode       = 'markers',
                    text       = df_by_color.iloc[:,0],
                    name       = str(i),
                    # opacity    = OPACITY,
                    hoverinfo  = 'text',
                    hoverlabel = dict(
                        bgcolor = 'lightgray'
                    ),
                    marker = dict(
                        size       = normalize_size(df_clean.iloc[:,4]),
                        sizemode   = 'diameter',
                        colorscale = COLORSCALE,
                        line       = dict(
                            width  = 0.00,
                        ),
                    )
                )
            )

    return traces

# If it is run as the main function
if __name__ == '__main__':
    print('')
