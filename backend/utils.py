def process_data(df):
    df = df.copy()

    # Remove missing
    df = df.dropna()

    # Ensure Date exists
    if 'Date' in df.columns:
        df['Date'] = df['Date'].astype(str)

    # Required columns check
    required = ['Open', 'Close', 'High', 'Low']
    for col in required:
        if col not in df.columns:
            raise Exception(f"{col} column missing")

    # Metrics
    df['Daily Return'] = (df['Close'] - df['Open']) / df['Open']
    df['MA7'] = df['Close'].rolling(7).mean()
    df['52W High'] = df['High'].rolling(252).max()
    df['52W Low'] = df['Low'].rolling(252).min()
    df['Volatility'] = df['Close'].rolling(7).std()

    return df