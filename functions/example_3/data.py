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
def get_labels(dframe, dataType):
    # Initialzie the labels
    x_labels = []
    y_labels = []
    size_labels = []

    if dataType == 1:
        x_labels = list(dframe)[0]
        for n in list(dframe)[1:]:
            y_labels.append(n)
            if dframe[n].dtype != 'object':
                size_labels.append(n)
    else:
        count = 0;
        for n in list(dframe)[0:]:
            if count == 1:
                y_labels.append(n)

                if dframe[n].dtype != 'object':
                    size_labels.append(n)
                count = 0
            else:
                x_labels.append(n)
                count = 1


    return x_labels, y_labels, size_labels

# If it is run as the main function
if __name__ == '__main__':
    print('')
