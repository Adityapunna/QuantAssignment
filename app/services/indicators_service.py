# services/indicators_service.py
import numpy as np
import pandas as pd
from config import DATA_DIR
from app.utils.data_related_utils import clean_stock_data
from config import DATE_COL,SYMBOL_COL,CLOSE_COL,SMA_COL,EMA_COL,RSI_COL,MACD_COL,SIGNAL_COL,HIST_COL,UPPER_BB_COL,LOWER_BB_COL


def calculate_simple_moving_average(df, stock_symbol, ma_period, start_date, end_date):
    """
    Calculate moving average for a specific stock symbol over a date range.

    Parameters:
        df (pd.DataFrame): DataFrame with columns ['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']
        stock_symbol (str): Stock ticker/symbol to filter
        ma_period (int): Moving average window (e.g. 20 for 20-day MA)
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
        pd.DataFrame: DataFrame with Date, Close, and Moving Average
    """
    # Filter and sort
    stock_df = df[df[SYMBOL_COL] == stock_symbol].sort_values(DATE_COL).copy()

    # Calculate moving average
    stock_df[SMA_COL] = stock_df[CLOSE_COL].rolling(window=ma_period).mean()

    # Filter by date range
    filtered_df = stock_df[(stock_df[DATE_COL] >= start_date) & (stock_df[DATE_COL] <= end_date)]

    # Reset index for clean output
    filtered_df = filtered_df.reset_index(drop=True)

    filtered_df[DATE_COL] = filtered_df[DATE_COL].astype(str)
    filtered_df = filtered_df.where(pd.notnull(filtered_df), None)
    filtered_df = filtered_df.replace({np.nan: None})

    return filtered_df[[SYMBOL_COL,DATE_COL, SMA_COL]]

def calculate_exponential_moving_average(df, stock_symbol, ema_period, start_date, end_date):
    """
    Calculate Exponential Moving Average (EMA) for a stock symbol over a date range.

    Parameters:
        df (pd.DataFrame): DataFrame with columns ['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']
        stock_symbol (str): Stock ticker/symbol to filter
        ema_period (int): EMA window (e.g., 20 for 20-day EMA)
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
        pd.DataFrame: DataFrame with Date, Close, and EMA
    """
    # Filter and sort by date
    stock_df = df[df[SYMBOL_COL] == stock_symbol].sort_values(DATE_COL).copy()

    # Calculate EMA using pandas ewm
    stock_df[EMA_COL] = stock_df[CLOSE_COL].ewm(span=ema_period, adjust=False).mean()

    # Filter by date range
    filtered_df = stock_df[(stock_df[DATE_COL] >= start_date) & (stock_df[DATE_COL] <= end_date)]

    # Reset index for clean output
    filtered_df = filtered_df.reset_index(drop=True)
    filtered_df[DATE_COL] = filtered_df[DATE_COL].astype(str)
    filtered_df = filtered_df.where(pd.notnull(filtered_df), None)
    filtered_df = filtered_df.replace({np.nan: None})

    return filtered_df[[SYMBOL_COL,DATE_COL, EMA_COL]]


def calculate_rsi(df, stock_symbol, rsi_period, start_date, end_date):
    """
    Calculate Relative Strength Index (RSI) for a stock over a date range.

    Parameters:
        df (pd.DataFrame): DataFrame with columns ['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']
        stock_symbol (str): Stock ticker/symbol to filter
        rsi_period (int): Period for RSI (e.g., 14 for 14-day RSI)
        start_date (str): Start date in 'YYYY-MM-DD' format
        end_date (str): End date in 'YYYY-MM-DD' format

    Returns:
        pd.DataFrame: DataFrame with Date, Close, and RSI
    """
    # Filter and sort
    stock_df = df[df[SYMBOL_COL] == stock_symbol].sort_values(DATE_COL).copy()

    # Calculate price change
    delta = stock_df[CLOSE_COL].diff()

    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate average gain/loss using exponential moving average
    avg_gain = gain.rolling(window=rsi_period, min_periods=rsi_period).mean()
    avg_loss = loss.rolling(window=rsi_period, min_periods=rsi_period).mean()

    # Use the Wilder smoothing (EMA after the first period)
    avg_gain = avg_gain.combine_first(gain.ewm(alpha=1/rsi_period, adjust=False).mean())
    avg_loss = avg_loss.combine_first(loss.ewm(alpha=1/rsi_period, adjust=False).mean())

    # Calculate RS and RSI
    rs = avg_gain / avg_loss
    stock_df[RSI_COL] = 100 - (100 / (1 + rs))

    # Filter by date range
    stock_df = stock_df[(stock_df[DATE_COL] >= start_date) & (stock_df[DATE_COL] <= end_date)]

    stock_df[DATE_COL] = stock_df[DATE_COL].astype(str)
    stock_df = stock_df.where(pd.notnull(stock_df), None)
    stock_df = stock_df.replace({np.nan: None})

    # Clean output
    return stock_df[[SYMBOL_COL,DATE_COL, RSI_COL]].reset_index(drop=True)


def calculate_macd(df, stock_symbol, fast_period=12, slow_period=26, signal_period=9, start_date=None, end_date=None):
    """
    Calculate MACD, Signal line, and Histogram for a stock over a date range.

    Parameters:
        df (pd.DataFrame): DataFrame with ['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']
        stock_symbol (str): Stock ticker/symbol to filter
        fast_period (int): Fast EMA period (default = 12)
        slow_period (int): Slow EMA period (default = 26)
        signal_period (int): Signal line EMA period (default = 9)
        start_date (str): Start date in 'YYYY-MM-DD' (optional)
        end_date (str): End date in 'YYYY-MM-DD' (optional)

    Returns:
        pd.DataFrame: DataFrame with Date, Close, MACD, Signal Line, and Histogram
    """
    # Filter for selected stock and sort by date
    stock_df = df[df[SYMBOL_COL] == stock_symbol].sort_values(DATE_COL).copy()

    # Calculate EMAs
    ema_fast = stock_df[CLOSE_COL].ewm(span=fast_period, adjust=False).mean()
    ema_slow = stock_df[CLOSE_COL].ewm(span=slow_period, adjust=False).mean()

    # MACD line
    stock_df[MACD_COL] = ema_fast - ema_slow

    # Signal line (9-period EMA of MACD)
    stock_df[SIGNAL_COL] = stock_df[MACD_COL].ewm(span=signal_period, adjust=False).mean()

    # Histogram = MACD - Signal
    stock_df[HIST_COL] = stock_df[MACD_COL] - stock_df[SIGNAL_COL]

    # Filter by date range if provided
    if start_date and end_date:
        stock_df = stock_df[(stock_df[DATE_COL] >= start_date) & (stock_df[DATE_COL] <= end_date)]

    stock_df[DATE_COL] = stock_df[DATE_COL].astype(str)
    stock_df = stock_df.where(pd.notnull(stock_df), None)
    stock_df = stock_df.replace({np.nan: None})

    return stock_df[[SYMBOL_COL, DATE_COL, MACD_COL, SIGNAL_COL, HIST_COL]].reset_index(drop=True)


def calculate_bollinger_bands(df, stock_symbol, period=20, num_std_dev=2, start_date=None, end_date=None):
    """
    Calculate Bollinger Bands (SMA, Upper Band, Lower Band) for a stock.

    Parameters:
        df (pd.DataFrame): DataFrame with ['Date', 'Symbol', 'Open', 'High', 'Low', 'Close', 'Volume']
        stock_symbol (str): Stock ticker/symbol to filter
        period (int): Moving average period (default = 20)
        num_std_dev (int): Standard deviation multiplier (default = 2)
        start_date (str): Start date in 'YYYY-MM-DD' (optional)
        end_date (str): End date in 'YYYY-MM-DD' (optional)

    Returns:
        pd.DataFrame: DataFrame with Date, Close, SMA, Upper Band, and Lower Band
    """
    # Filter and sort by date
    stock_df = df[df[SYMBOL_COL] == stock_symbol].sort_values(DATE_COL).copy()

    # Calculate SMA and standard deviation
    stock_df[SMA_COL] = stock_df[CLOSE_COL].rolling(window=period).mean()
    rolling_std = stock_df[CLOSE_COL].rolling(window=period).std()

    # Calculate upper and lower bands
    stock_df[UPPER_BB_COL] = stock_df[SMA_COL] + (rolling_std * num_std_dev)
    stock_df[LOWER_BB_COL] = stock_df[SMA_COL] - (rolling_std * num_std_dev)

    # Filter by date range if provided
    if start_date and end_date:
        stock_df = stock_df[(stock_df[DATE_COL] >= start_date) & (stock_df[DATE_COL] <= end_date)]

    stock_df[DATE_COL] = stock_df[DATE_COL].astype(str)
    stock_df = stock_df.where(pd.notnull(stock_df), None)
    stock_df = stock_df.replace({np.nan: None})

    return stock_df[[SYMBOL_COL, DATE_COL, SMA_COL, UPPER_BB_COL, LOWER_BB_COL]].reset_index(drop=True)
#
# def simple_moving_average(input_path,MA,DATE_RANGE):
#     try:
#         df = pd.read_parquet(input_path)
#
#
#     except Exception as e:
#         print(f"Error: {e}")


if __name__ == "__main__":
    input_path = DATA_DIR / "stocks_ohlc_data.parquet"
    # output_path = DATA_DIR / "stocks_ohlc_data.csv"
    # data_cleaning(input_path, output_path)

    df = pd.read_parquet(input_path)
    df = clean_stock_data(df)
    # result_df = calculate_simple_moving_average(
    #     df=df,
    #     stock_symbol='RAMASTEEL',
    #     ma_period=20,
    #     start_date='2022-07-22',
    #     end_date='2022-12-31'
    # )
    # result_df = calculate_exponential_moving_average(
    #     df=df,
    #     stock_symbol='RAMASTEEL',
    #     ema_period=20,
    #     start_date='2022-07-22',
    #     end_date='2022-12-31'
    # )
    # result_df = calculate_rsi(
    #     df=df,
    #     stock_symbol='RAMASTEEL',
    #     rsi_period=20,
    #     start_date='2022-07-22',
    #     end_date='2022-12-31'
    # )
    # result_df = calculate_macd(
    #     df=df,
    #     stock_symbol='RAMASTEEL',
    #     fast_period=12, slow_period=26, signal_period=9,
    #     start_date='2022-07-22',
    #     end_date='2022-12-31'
    # )
    result_df = calculate_bollinger_bands(
        df=df,
        stock_symbol='RAMASTEEL',
        period=20, num_std_dev=2,
        start_date='2022-07-22',
        end_date='2022-12-31'
    )

    # print("NaNs per column:\n", result_df.isna().sum())
    # print("Inf per column:\n", (result_df == np.inf).sum())
    # print("-Inf per column:\n", (result_df == -np.inf).sum())
    # print(~np.isfinite(result_df))  # Where is it non-finite?
    # result_df = result_df.where(pd.notnull(df), None)
    a = result_df.to_dict(orient="records")
    print(a)
