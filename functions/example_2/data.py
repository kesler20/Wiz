##==================================
## External imports
##==================================
import pandas as pd

##==================================
## Internal imports
##==================================
from functions.global_functions import *

##==================================
## Functions
##==================================
def get_labels(dframe):
    # Initialzie the labels
    labels = []
    size_labels = []

    # Get the labels from the file (can't be categorical in size)
    labels = list(dframe)[1:]
    size_labels = list(dframe.iloc[:,1:].select_dtypes(exclude = 'object'))

    return labels, size_labels


# Clean the data and make the datatable
def clean_data_static(df, x_column, y_column, c_column,s_column, z_column, z_off):
    # Reduce data to what needs to be plotted or displayed in the table
    if x_column is not None and y_column is not None and c_column is not None and s_column is not None:
        if z_off:
            # 2D plot
            df_new = df[[df.columns[0], x_column, y_column, c_column, s_column ]]
        else:
            # 3D plot
            df_new = df[[df.columns[0], x_column, y_column, c_column, s_column, z_column ]]

    elif x_column is not None and y_column is not None and c_column is not None:
        df_new = df[[df.columns[0], x_column, y_column, c_column ]]

    elif x_column is not None and y_column is not None:
        df_new = df[[df.columns[0], x_column, y_column ]]

    elif x_column is not None:
        df_new = df[[df.columns[0], x_column]]

    else:
        df_new = df[[df.columns[0]]]

    return df_new


# Get the axis ranges from the last sheet
def get_ranges(data, x_type, y_type, x_column, y_column, z_column):
    # Get the maximum data to set the layout
    num_sheets = len(list(data))-1

    # Get the values
    min_x = float(data[list(data)[num_sheets]][[x_column]].min())
    max_x = float(data[list(data)[num_sheets]][[x_column]].max())
    min_y = float(data[list(data)[num_sheets]][[y_column]].min())
    max_y = float(data[list(data)[num_sheets]][[y_column]].max())
    min_z = float(data[list(data)[num_sheets]][[z_column]].min())
    max_z = float(data[list(data)[num_sheets]][[z_column]].max())

    # Some deviation from the exact range
    delta_x = 0.05*(max_x - min_x)
    delta_y = 0.05*(max_y - min_y)
    delta_z = 0.05*(max_z - min_z)

    # Get ranges
    x_range = [min_x - delta_x, max_x + delta_x]
    y_range = [min_y - delta_y, max_y + delta_y]
    z_range = [min_z - delta_z, max_z + delta_z]

    # Change range if the axis is logarithmic
    if 'log' in x_type:
        min_x = data[list(data)[num_sheets]][[x_column]][data[list(data)[num_sheets]][[x_column]] > 0].min()
        delta_x = abs(0.1*(log10(max_x) - log10(min_x)))
        x_range = [log10(min_x) - delta_x, log10(max_x) + delta_x]

    if 'log' in y_type:
        min_y = data[list(data)[num_sheets]][[y_column]][data[list(data)[num_sheets]][[y_column]] > 0].min()
        delta_y = abs(0.1*(log10(max_y) - log10(min_y)))
        y_range = [log10(min_y) - delta_y, log10(max_y) + delta_y]

    return x_range, y_range, z_range

# If it is run as the main function
if __name__ == '__main__':
    print('')
