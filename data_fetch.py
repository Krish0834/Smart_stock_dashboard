# data_fetch.py

import yfinance as yf
import pandas as pd
import ssl
import ta

ssl._create_default_https_context = ssl._create_unverified_context

def fetch_stock_data(ticker="TCS.NS", period="1y", interval="1d"):
    df = yf.download(ticker, period=period, interval=interval, auto_adjust=False)

    df.columns.name = None  # remove 'Price'
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]  # Flatten multi-index

    df = df.dropna()
    df[['Open', 'High', 'Low', 'Close', 'Volume']] = df[['Open', 'High', 'Low', 'Close', 'Volume']].astype(float)

     # Add indicators
    df['EMA20'] = ta.trend.ema_indicator(df['Close'], window=20)
    df['EMA50'] = ta.trend.ema_indicator(df['Close'], window=50)
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()

    df = generate_signals(df)
    return df

def generate_signals(df):
    df['Signal'] = 0  # Default = hold

    # Buy signal: EMA20 crosses above EMA50
    df.loc[
        (df['EMA20'] > df['EMA50']) &
        (df['EMA20'].shift(1) <= df['EMA50'].shift(1)),
        'Signal'
    ] = 1

    # Sell signal: EMA20 crosses below EMA50
    df.loc[
        (df['EMA20'] < df['EMA50']) &
        (df['EMA20'].shift(1) >= df['EMA50'].shift(1)),
        'Signal'
    ] = -1

    return df


  
