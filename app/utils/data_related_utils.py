import pandas as pd
from config import DATA_DIR, SYMBOL_COL, DATE_COL,OPEN_COL,HIGH_COL,LOW_COL,CLOSE_COL


# def convert_parquet_to_csv(input_path: str, output_path: str):
#     """Convert a Parquet file to CSV, with basic validation."""
#     if not input_path.exists():
#         print(f"Input file not found: {input_path}")
#         return
#     if input_path.suffix != ".parquet" or output_path.suffix != ".csv":
#         print("Please use .parquet as input and .csv as output.")
#         return
#
#     try:
#         df = pd.read_parquet(input_path)
#         df.to_csv(output_path, index=False)
#         print(f"Converted: {input_path} → {output_path}")
#
#
#     except Exception as e:
#         print(f"Error: {e}")

# def validate_stock_data(df: pd.DataFrame):
#     missing = df.isnull().sum()
#     if missing.any():
#         print("Warning: Missing data detected!")
#         print(missing[missing > 0])
#     else:
#         print("No missing values found.")


def clean_stock_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean stock OHLC data by handling missing values smartly.
    - Fills missing OHLC with forward/backward fill per stock.
    - Fills missing volume with 0.
    - Drops rows missing symbol or date.
    - Prints summary of changes.

    Returns:
        Cleaned DataFrame.
    """

    df.columns = [col.strip().lower() for col in df.columns]

    print("🔍 Initial missing values:")
    print(df.isnull().sum())

    df = df.dropna(subset=[SYMBOL_COL, DATE_COL])
    df[DATE_COL] = pd.to_datetime(df[DATE_COL])
    df = df.sort_values([SYMBOL_COL, DATE_COL])

    df[[OPEN_COL, HIGH_COL, LOW_COL, CLOSE_COL]] = (
        df.groupby(SYMBOL_COL)[[OPEN_COL, HIGH_COL, LOW_COL, CLOSE_COL]]
        .apply(lambda g: g.ffill().bfill())
        .reset_index(drop=True)
    )

    # if 'volume' in df.columns:
    #     df['volume'] = df['volume'].fillna(0)

    print("\n✅ Missing values after cleaning:")
    print(df.isnull().sum())

    return df


def data_cleaning(input_path):
    try:
        df = pd.read_parquet(input_path)
        after_clean_df = clean_stock_data(df)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    input_path = DATA_DIR / "stocks_ohlc_data.parquet"
    # output_path = DATA_DIR / "stocks_ohlc_data.csv"
    # convert_parquet_to_csv(input_path, output_path)
    data_cleaning(input_path)