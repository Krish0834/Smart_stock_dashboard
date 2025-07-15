import streamlit as st
from data_fetch import fetch_stock_data
from visualizer import plot_candle_volume_with_ema_and_signals


# --- UI Sidebar ---
st.sidebar.title("📈 Stock Signal Dashboard")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="TCS.NS")
period = st.sidebar.selectbox("Select Period", ["1mo", "3mo", "6mo", "1y"], index=3)
interval = st.sidebar.selectbox("Interval", ["1d", "1wk"], index=0)
show_rsi = st.sidebar.checkbox("Show RSI Data in Table", value=False)

# --- Title ---
st.title(f"📊 {ticker} Signal Dashboard")

# --- Fetch Data ---
with st.spinner("Fetching data..."):
    df = fetch_stock_data(ticker, period=period, interval=interval)

# --- Show Chart ---
if df.empty:
    st.error("No data available. Check ticker or time range.")
else:
    st.success("Data fetched successfully!")
    plot_candle_volume_with_ema_and_signals(df, ticker)
    
    st.subheader("📋 Latest Signal Summary")
    st.write(df[['Close', 'EMA20', 'EMA50', 'RSI', 'Signal']].tail(10))

    if show_rsi:
        st.subheader("📈 RSI Data")
        st.line_chart(df['RSI'])
