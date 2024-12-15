from Utils.import_packages import *

# Calculate excess return sentiment label
def excess_return_sentiment_label(stock_data, market_data, num_days=3, price_used="Adj Close"):
    if price_used not in stock_data.columns or price_used not in market_data.columns:
        raise ValueError(f"Column '{price_used}' is missing in stock or market data.")

    stock_df = stock_data[[price_used]].copy()
    market_df = market_data[[price_used]].copy()
    market_df = market_df.add_prefix("SPY_")
    merged_df = stock_df.join(market_df)
    merged_df = merged_df.pct_change()


    merged_df["excess_returns"] = merged_df["Adj Close"] - merged_df["SPY_Adj Close"]
    merged_df["X_days_excess_returns"] =\
        (
            (1 + merged_df["excess_returns"])
            .rolling(num_days)
            .apply(lambda x: x.cumprod()[-1], raw=True)
            .shift(-(num_days - 1))
            - 1
        )

    # Label for 1 excess returns > 0, 0 otherwise
    merged_df["sentiment_label"] = (merged_df["X_days_excess_returns"] > 0).astype(int)
    merged_df = merged_df.reset_index()
    merged_df = merged_df[["Date", "sentiment_label"]]
    return merged_df