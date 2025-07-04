# config.py
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "app" / "data"
print(BASE_DIR)  # C:\Users\Dell\PycharmProjects\QuantAssignment
print(DATA_DIR)


# Column name constants
DATE_COL = 'date'
SYMBOL_COL = 'symbol'
OPEN_COL = 'open'
HIGH_COL = 'high'
LOW_COL = 'low'
CLOSE_COL = 'close'
VOLUME_COL = 'volume'

# Indicator columns
SMA_COL = 'sma'
EMA_COL = 'ema'
RSI_COL = 'rsi'
UPPER_BB_COL = 'uboll'
LOWER_BB_COL = 'lboll'
MACD_COL = 'macd'
SIGNAL_COL = 'signal'
HIST_COL = 'hist'

# Indicator config defaults
DEFAULT_SMA_PERIOD = 20
DEFAULT_RSI_PERIOD = 14