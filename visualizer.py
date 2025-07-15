# visualizer.py

import plotly.graph_objects as go

def plot_candle_volume_with_ema_and_signals(df, ticker="Stock"):
    fig = go.Figure()
    print(df[['Open', 'High', 'Low', 'Close']].tail(10))
    print(df[['Open', 'High', 'Low', 'Close']].describe())


    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Candles"
    ))

    # Volume as bar chart (separate axis)
    fig.add_trace(go.Bar(
        x=df.index,
        y=df['Volume'],
        name='Volume',
        marker=dict(color='rgba(128, 128, 128, 0.3)'),
        yaxis='y2'
    ))

    
    # EMA 20
    fig.add_trace(go.Scatter(
        x=df.index, y=df['EMA20'], mode='lines', name='EMA20',
        line=dict(color='blue', width=1)
    ))

    # EMA 50
    fig.add_trace(go.Scatter(
        x=df.index, y=df['EMA50'], mode='lines', name='EMA50',
        line=dict(color='orange', width=1)
    ))

    
    # ✅ Buy signals (green arrow up)
    buy = df[df['Signal'] == 1]
    fig.add_trace(go.Scatter(
        x=buy.index, y=buy['Close'],
        mode='markers',
        marker=dict(color='green', symbol='arrow-up', size=12),
        name='Buy Signal'
    ))

    # ✅ Sell signals (red arrow down)
    sell = df[df['Signal'] == -1]
    fig.add_trace(go.Scatter(
        x=sell.index, y=sell['Close'],
        mode='markers',
        marker=dict(color='red', symbol='arrow-down', size=12),
        name='Sell Signal'
    ))


      # Layout
    fig.update_layout(
        title=f"{ticker} Price + Volume + EMA + Signals",
        xaxis=dict(rangeslider_visible=False),
        yaxis=dict(title="Price"),
        yaxis2=dict(
            overlaying='y',
            side='right',
            showgrid=False,
            title='Volume'
        ),
        height=700
    )
    fig.show()
