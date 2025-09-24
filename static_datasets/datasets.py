import datetime as dt
import pandas as pd
import yfinance as yf

# ===============
# Examples 1 & 2
# ===============
example_1 = pd.read_excel("static_datasets/O2_Data.xlsx", sheet_name=None)
example_2 = pd.read_excel("static_datasets/O2_Data.xlsx", sheet_name=None)

# ===============
# Example 3
# ===============
TICKERS = ["AAPL", "AMZN", "NFLX", "META", "MSFT", "NVDA", "BABA", "GOOG", "TSLA"]

start = dt.date(2010, 1, 1)
end = dt.date(2020, 6, 10)

def fetch_close_series(ticker: str, start_date, end_date) -> pd.Series | None:
    """
    Fetch 'Close' prices for a single ticker via yfinance.
    Returns a Series named <ticker> indexed by Date, or None on failure/empty.
    """
    try:
        df = yf.download(
            ticker,
            start=start_date,
            end=end_date,
            auto_adjust=False,
            progress=False,
            threads=False,
        )
        if df is None or df.empty or "Close" not in df.columns:
            return None
        s = df["Close"].copy()
        s.name = ticker  # important: avoid duplicate 'Close' column names
        return s
    except Exception:
        return None

series_list: list[pd.Series] = []
for t in TICKERS:
    s = fetch_close_series(t, start, end)
    if s is not None:
        series_list.append(s)
    else:
        # Create an empty placeholder with the right name so concat still works
        series_list.append(pd.Series(name=t, dtype="float64"))

# Concatenate all tickers by date index
example_3 = pd.concat(series_list, axis=1)

# Ensure a proper Date column regardless of index name
example_3 = example_3.reset_index()
if "index" in example_3.columns and "Date" not in example_3.columns:
    example_3 = example_3.rename(columns={"index": "Date"})
elif "Date" not in example_3.columns:
    # If the DatetimeIndex had no name, reset_index() creates 'index'
    example_3 = example_3.rename(columns={example_3.columns[0]: "Date"})

# ===============
# Example 4
# ===============
example_4 = pd.read_excel("static_datasets/Wine.xlsx", sheet_name=None)

# ===============
# Example 5
# ===============
example_5 = pd.read_excel("static_datasets/Iris.xlsx", sheet_name=None)
