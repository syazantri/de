import pandas as pd
from src.utils import get_logger

logger = get_logger(__name__)


def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df["transaction_id"] = df["transaction_id"].str.strip()
    df["user_id"] = df["user_id"].str.strip()
    df["merchant_id"] = df["merchant_id"].str.strip()
    df["transaction_timestamp"] = pd.to_datetime(df["transaction_timestamp"])
    df["amount"] = df["amount"].astype(float).round(2)
    df["currency"] = df["currency"].str.strip().str.upper()
    df["payment_method"] = df["payment_method"].str.strip()
    df["transaction_status"] = df["transaction_status"].str.strip().str.upper()
    df["created_at"] = pd.to_datetime(df["created_at"])

    logger.info(f"Transformed {len(df)} rows")
    return df
