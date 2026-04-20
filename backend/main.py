
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from data import fetch_stock_data
from utils import process_data

app = FastAPI(title="Stock Data Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home route
@app.get("/")
def home():
    return {"message": "API is running 🚀"}

# 1. Companies list
@app.get("/companies")
def get_companies():
    return ["TCS", "INFY", "RELIANCE", "HDFCBANK"]

# 2. Last 30 days data
@app.get("/data/{symbol}")
def get_stock_data(symbol: str):
    try:
        df = fetch_stock_data(symbol + ".NS")
        df = process_data(df)

        return df.tail(30).fillna(0).to_dict(orient="records")

    except Exception as e:
        return {"error": str(e)}
# 3. Summary
@app.get("/summary/{symbol}")
def get_summary(symbol: str):
    df = fetch_stock_data(symbol + ".NS")
    df = process_data(df)

    return {
    "52_week_high": float(df['High'].max() or 0),
    "52_week_low": float(df['Low'].min() or 0),
    "average_close": float(df['Close'].mean() or 0)
}

# 4. Compare (Bonus)
@app.get("/compare")
def compare(symbol1: str, symbol2: str):
    df1 = fetch_stock_data(symbol1 + ".NS")
    df2 = fetch_stock_data(symbol2 + ".NS")

    return {
        symbol1: float(df1['Close'].iloc[-1]),
        symbol2: float(df2['Close'].iloc[-1])
    }
@app.get("/top-movers")
def top_movers():
    stocks = ["TCS.NS", "INFY.NS", "RELIANCE.NS"]

    results = []

    for stock in stocks:
        df = fetch_stock_data(stock)
        df = process_data(df)

        latest = df.iloc[-1]
        results.append({
            "symbol": stock,
            "return": float(latest["Daily Return"])
        })

    sorted_data = sorted(results, key=lambda x: x["return"], reverse=True)

    return {
        "top_gainer": sorted_data[0],
        "top_loser": sorted_data[-1]
    }