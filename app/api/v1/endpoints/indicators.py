from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
import pandas as pd

from app.utils.data_related_utils import clean_stock_data
from app.services.indicators_service import (
    calculate_simple_moving_average,
    calculate_exponential_moving_average,
    calculate_rsi,
    calculate_macd,
    calculate_bollinger_bands
)
from config import DATA_DIR, DATE_COL
from app.services.auth_service import get_current_user
from app.db.database import get_db
from app.services.tier_access_service import check_access
from app.db.models import User

router = APIRouter()

def load_and_clean_data():
    df = pd.read_parquet(DATA_DIR / "stocks_ohlc_data.parquet")
    return clean_stock_data(df)

@router.get("/hello")
def hello_world():
    return {"message": "Hello, World!"}

@router.get("/indicators/sma")
def get_sma(
    stock_symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    period: int = Query(20),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    print("entered sma")
    check_access(user, "SMA", start_date, end_date)
    df = load_and_clean_data()
    result_df = calculate_simple_moving_average(df, stock_symbol, period, start_date, end_date)
    user.requests_today += 1
    db.commit()
    return result_df.to_dict(orient="records")

@router.get("/indicators/ema")
def get_ema(
    stock_symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    period: int = Query(20),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    check_access(user, "EMA", start_date, end_date)
    df = load_and_clean_data()
    result_df = calculate_exponential_moving_average(df, stock_symbol, period, start_date, end_date)
    user.requests_today += 1
    db.commit()
    return result_df.to_dict(orient="records")

@router.get("/indicators/rsi")
def get_rsi(
    stock_symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    period: int = Query(14),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    check_access(user, "RSI", start_date, end_date)
    df = load_and_clean_data()
    result_df = calculate_rsi(df, stock_symbol, period, start_date, end_date)
    user.requests_today += 1
    db.commit()
    return result_df.to_dict(orient="records")

@router.get("/indicators/macd")
def get_macd(
    stock_symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    fast_period: int = Query(12),
    slow_period: int = Query(26),
    signal_period: int = Query(9),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    check_access(user, "MACD", start_date, end_date)
    df = load_and_clean_data()
    result_df = calculate_macd(df, stock_symbol, fast_period, slow_period, signal_period, start_date, end_date)
    user.requests_today += 1
    db.commit()
    return result_df.to_dict(orient="records")

@router.get("/indicators/bollinger")
def get_bollinger(
    stock_symbol: str = Query(...),
    start_date: str = Query(...),
    end_date: str = Query(...),
    period: int = Query(20),
    num_std_dev: int = Query(2),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    check_access(user, "Bollinger", start_date, end_date)
    df = load_and_clean_data()
    result_df = calculate_bollinger_bands(df, stock_symbol, period, num_std_dev, start_date, end_date)
    user.requests_today += 1
    db.commit()
    return result_df.to_dict(orient="records")