##==================================
## External imports
##==================================
import pandas as pd
import numpy as np
import sklearn
from sklearn.decomposition import PCA as sklearnPCA
from sklearn.preprocessing import StandardScaler
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

##==================================
## Internal imports
##==================================
from functions.global_functions import *


##==================================
## Functions
##==================================
def input_to_df(contents, filename):
    # Allow .csv, .xls or .xlsx files
    if '.csv' in filename[0] or '.dat' in filename[0] or '.txt' in filename[0]:
        # Initialize filenames and output data type
        sheets = []
        df = dict()

        for i in range(len(filename)):
            # Add file as if it were a sheet
            sheets.append(filename[i].split('.csv')[0])

            # Get info on file
            contents_type, content_string = contents[i].split(',')
            decoded = base64.b64decode(content_string)

            # Add dataframe to dict with filename as key
            df_temp = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

            # Convert to JSON
            df[sheets[i]] = df_temp

    elif '.xls' in filename[0]:
        # Get file info
        contents_type, content_string = contents[0].split(',')
        decoded = base64.b64decode(content_string)

        # Read in file
        df= pd.read_excel(io.BytesIO(decoded), sheet_name = None)

    else:
        df = dict()

    return df


def get_labels(dframe):
    # Initialzie the labels
    class_labels = []

    # Class labels can only be categorical or a variable with less than 10 unique values
    for n in list(dframe):
        if 'object' == dframe[n].dtype:
            class_labels.append(n)
        elif len(dframe[n].unique()) < 10:
            class_labels.append(n)

    return class_labels

# Clean the data and make the datatable
def make_data_table(df, selected_rows):

    # Convert get a table object from the dataframe
    table_out = df_to_table(df, selected_rows)

    return table_out


def df_to_table(df, selected_rows):
    # Make columns unique for data table
    df_new = unique_columns(df)

    table_out = dt.DataTable(
        id = 'pca-data-table-plot',
        data = df_new.to_dict('records'),
        columns = [{"name": i, "id": i} for i in df_new.columns],

        filtering = True,
        sorting = True,
        row_selectable= 'multi',
        selected_rows=selected_rows,
        n_fixed_rows=1,

        style_table={'overflowX': 'scroll'},
        style_cell={'padding': '5px'},
        style_cell_conditional=[
        {
            'if': {'column_id': 'Labels'},
            'textAlign': 'left'
        }]
    )
    return table_out

def empty_table(id):
    table_out = dt.DataTable(
        id = id,
        data = [{}],
        row_selectable = 'multi',
        selected_rows = []
    )
    return table_out


# Filter data
def filter_data(table_data, selected_rows):
    # Convert data to Dataframe
    df = pd.DataFrame.from_records(table_data)

    # Get the original column titles back
    df = ununique_columns(df)

    # Only plot selected points
    if selected_rows is None or not selected_rows:
        plot_data = df
    else:
        plot_data = df.iloc[selected_rows]

    return plot_data

# Principle component analysis on data
def PCA(df, class_name):
    # Cannot do PCA on an empty matrix
    if len(list(df)) < 2:
        return df, [], [], []

    # Figure out which columns can be considered (only float or int columns but not the class column)
    cols = []
    for item in list(df):
        if 'float' in df[item].dtypes.name:
            if item != class_name:
                cols.append(df.columns.get_loc(item))

    # Get new dataframe
    df_new = df[df.columns[cols]]

    # Set this as the data to analyze
    X = df_new.values

    # Standardize the data
    X_std = StandardScaler().fit_transform(X)

    # Do PCA
    pca = sklearnPCA(n_components = len(list(df_new)))
    Y = pca.fit_transform(X_std)

    ## Get variance contributions
    var_exp = pca.explained_variance_ratio_
    cum_var_exp = pca.explained_variance_ratio_.cumsum()

    return Y, var_exp, cum_var_exp

def LDA(df, class_name):
    # Cannot do PCA on an empty matrix
    if len(list(df)) < 2:
        return df, [], [], []

    # Figure out which columns can be considered (only float or int columns but not the class column)
    cols = []
    for item in list(df):
        if 'float' in df[item].dtypes.name:
            if item != class_name:
                cols.append(df.columns.get_loc(item))

    # Get new dataframe
    df_new = df[df.columns[cols]]

    # Set this as the data to analyze
    X = df_new.values

    # LDA
    n = min(len(list(df_new)), len(df[class_name].unique()) - 1)
    lda = LinearDiscriminantAnalysis(n_components = n)
    Y_lda = lda.fit_transform(X, df[class_name])
    exp_var = lda.explained_variance_ratio_
    cum_var = lda.explained_variance_ratio_.cumsum()

    return Y_lda, exp_var, cum_var

# If it is run as the main function
if __name__ == '__main__':
    print('')
