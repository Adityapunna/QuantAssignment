import pandas as pd

from app.utils import clean_stock_data
from config import DATA_DIR


def load_and_clean_data():
    df = pd.read_parquet(DATA_DIR / "stocks_ohlc_data.parquet")
    return clean_stock_data(df)