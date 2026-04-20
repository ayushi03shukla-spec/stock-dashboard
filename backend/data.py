import yfinance as yf
import pandas as pd

def fetch_stock_data(symbol):
    df = yf.download(symbol, period="1y")

    # 🔥 FIX: flatten columns if MultiIndex
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.reset_index(inplace=True)

    return df