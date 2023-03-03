import pandas as pd
import yfinance as yf
yf.pdr_override()
import pandas_datareader.data as webDR
import datetime as dt

#===============
# Examples 1 & 2
#===============
example_1 = pd.read_excel('static_datasets/O2_Data.xlsx', sheet_name = None)
example_2 = pd.read_excel('static_datasets/O2_Data.xlsx', sheet_name = None)

#===============
# Example 3
#===============
all_columns = ["AAPL","AMZN","NFLX","FB","MSFT","NVDA","BABA","GOOG","TSLA","DIS"];

# Initialize dataframe
example_3 = pd.DataFrame()

# Get the date range
start = dt.date(2010, 1, 1)
end = dt.date(2020, 6, 10)

# Loop through and fill with data
for ticker in all_columns:
    # Get data
    temp_df = webDR.get_data_yahoo(ticker, start = start, end = end)

    # Append to dataframe
    example_3 = pd.concat([example_3, temp_df['Close']], axis=1)
    example_3.rename({'Close': ticker}, axis=1, inplace=True)

# Change dates from index to column
example_3.reset_index(inplace = True, drop = False)
example_3.rename({'index': 'Date'}, axis=1, inplace=True)


#===============
# Example 4
#===============
example_4 = pd.read_excel('static_datasets/Wine.xlsx', sheet_name = None)

#===============
# Example 5
#===============
example_5 = pd.read_excel('static_datasets/Iris.xlsx', sheet_name = None)
