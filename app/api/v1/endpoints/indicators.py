from fastapi import APIRouter, Query
from typing import Optional
import pandas as pd
from app.utils.data_related_utils import clean_stock_data
from app.services.indicators_service import (
    calculate_simple_moving_average,
    calculate_exponential_moving_average,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands
)
from config import DATA_DIR,DATE_COL

router = APIRouter()
print("indicators.py file opened")

@router.get("/hello")
def hello_world():
    print("entered hello function")
    return {"message": "Hello, World!"}

@router.get("/sma")
def get_sma(
    stock_symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    period: int = Query(20)
):
    print("entered sma function")
    df = pd.read_parquet(DATA_DIR / "stocks_ohlc_data.parquet")
    df = clean_stock_data(df)
    result_df = calculate_simple_moving_average(df, stock_symbol, period, start_date, end_date)

    print("Result columns:", result_df.columns)
    print(result_df)
    # result_df[DATE_COL] = result_df[DATE_COL].astype(str)
    return result_df.to_json(orient="records")

@router.get("/ema")
def get_ema(
    stock_symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    period: int = Query(20)
):
    df = pd.read_parquet(DATA_DIR / "stocks_ohlc_data.parquet")
    df = clean_stock_data(df)
    result_df = calculate_exponential_moving_average(df, stock_symbol, period, start_date, end_date)
    # result_df[DATE_COL] = result_df[DATE_COL].astype(str)
    return result_df.to_json(orient="records")

@router.get("/rsi")
def get_rsi(
    stock_symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    period: int = Query(14)
):
    df = pd.read_parquet(DATA_DIR / "stocks_ohlc_data.parquet")
    df = clean_stock_data(df)
    result_df = calculate_rsi(df, stock_symbol, period, start_date, end_date)
    # result_df[DATE_COL] = result_df[DATE_COL].astype(str)
    return result_df.to_json(orient="records")

@router.get("/macd")
def get_macd(
    stock_symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    fast_period: int = Query(12),
    slow_period: int = Query(26),
    signal_period: int = Query(9)
):
    df = pd.read_parquet(DATA_DIR / "stocks_ohlc_data.parquet")
    df = clean_stock_data(df)
    result_df = calculate_macd(df, stock_symbol, fast_period, slow_period, signal_period, start_date, end_date)
    # result_df[DATE_COL] = result_df[DATE_COL].astype(str)
    return result_df.to_json(orient="records")

@router.get("/bollinger")
def get_bollinger(
    stock_symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    period: int = Query(20),
    num_std_dev: int = Query(2)
):
    df = pd.read_parquet(DATA_DIR / "stocks_ohlc_data.parquet")
    df = clean_stock_data(df)
    result_df = calculate_bollinger_bands(df, stock_symbol, period, num_std_dev, start_date, end_date)

    return result_df.to_json(orient="records")
