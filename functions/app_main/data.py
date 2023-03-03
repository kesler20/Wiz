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
# Get the axis labels
def get_labels(dframe):
    # Initialzie the labels
    labels = []
    size_labels = []

    # Get the labels from the file (can't be categorical in size)
    labels = list(dframe)[1:]
    size_labels = list(dframe.iloc[:,1:].select_dtypes(exclude = 'object'))

    return labels, size_labels

# Clean the data and make the datatable
def make_data_table(plot_data, selected_rows, filter_query, sort_by):
    return df_to_table('main-data-table-plot', plot_data, selected_rows, filter_query, sort_by)


# Clean the data and make the datatable
def get_plot_data(df, x_column, y_column, c_column,s_column, z_column, z_off):
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

    df_new = unique_columns(df_new)
    return df_new

# If it is run as the main function
if __name__ == '__main__':
    print('')
